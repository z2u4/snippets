
import datetime
import os
from sched import scheduler
import tomllib
import typing
import time
import threading
from autoplayer.debug import Debug
from zrcl4.subprocess import exec_command
import autoplayer.utils as utils
from autoplayer.model import Task

class AutoPlayer:   
    debugManager : Debug

    def __init__(
        self,
        configPath : str,
        runtimePaths : typing.List[str] = None, 
        overwriteCurrentTime : datetime.datetime = None
    ):
        self.__currentlyRunning = []
        self.__currentlyPending = []

        self.__configPath = configPath

        with open(self.__configPath, 'rb') as f:
            self.__config = tomllib.load(f)

        #TODO
        self.__runtimePaths = runtimePaths

        if isinstance(overwriteCurrentTime, datetime.time):
            overwriteCurrentTime = datetime.datetime.now().replace(hour=overwriteCurrentTime.hour, minute=overwriteCurrentTime.minute, second=0, microsecond=0)
        self.__overwriteCurrentTime = overwriteCurrentTime if overwriteCurrentTime else datetime.datetime.now()

        # debug
        self.debugManager = Debug(**self.__config.get("debug", {}))

        # scheduler
        self.__scheduler = scheduler(time.time, time.sleep)
        self.__mutex = threading.Lock()

        self.__parseConfig()
        if self.__currentlyPending:
            self.__autoScreenshot()

    def __autoScreenshot(self):
        if self.isRunning():
            self.debugManager.dscreenshot()
        if not self.__scheduler.queue:
            return
        self.__scheduler.enter(300, 1, self.__autoScreenshot)

    def __parseConfig(self):
        for task in self.__config.get("task", []):

            task : Task

            # check skip
            if "skip" in task and task["skip"]:
                print("Skipping task", task["name"])
                continue

            # check expire
            if "expire" in task:
                expire = datetime.datetime.strptime(task["expire"], "%Y-%m-%d").date()
                if expire < self.__overwriteCurrentTime.date():
                    print("Task", task["name"], "has expired")
                    continue
            
            # check past time
            at = task.get("at", None)
            at = datetime.datetime.strptime(at, "%I%M %p") if at else None
            if not at:
                print("No 'at' time specified for task", task["name"])
                continue

            scheduled_time = datetime.datetime.combine(self.__overwriteCurrentTime.date(), at.time())
            if scheduled_time < self.__overwriteCurrentTime:
                print("Task ", task["name"], "will not run at ", scheduled_time)
                continue

            print("Scheduling task", task["name"], "at", scheduled_time)
            print("Pending for", (scheduled_time - self.__overwriteCurrentTime).total_seconds()/60, "minutes")

            self.__currentlyPending.append(task)
            self.__scheduler.enter((scheduled_time - self.__overwriteCurrentTime).total_seconds(), 1, self.__runThread, (task,))

    def __handleActions(self, actions : typing.List[dict]):
        def fetchValue(data : typing.Union[str, typing.List[str]]):
            if isinstance(data, list):
                for key in data:
                    if key not in os.environ:
                        continue

                    return os.environ[key]
                return

            if data.upper() == data:
                return os.environ[data]
            
            return data    
    
        for action in actions:
            match action["type"]:
                case "ldplayer9_start":
                    utils.ldplayer_start(
                        utils.ldplayer9(),
                        fetchValue(action["val"])
                    )
                case "ldplayer4_start":
                    utils.ldplayer_start(
                        utils.ldplayer4(),
                        fetchValue(action["val"])
                    )
                case "ldplayer9_startex":
                    utils.ldplayer_startex(
                        utils.ldplayer9(),
                        fetchValue(action["pkg"]),
                        fetchValue(action["name"]),
                    )
                case "ldplayer4_startex":
                    utils.ldplayer_startex(
                        utils.ldplayer4(),
                        fetchValue(action["pkg"]),
                        fetchValue(action["name"])
                    )
                case "run":
                    if "args" in action:
                        args = fetchValue(action["args"])
                    os.startfile(fetchValue(action["val"]), arguments=args)
                case "process_kill" | "kill":
                    utils.process_kill(fetchValue(action["val"]))
                case "script":
                    utils.handle_script(fetchValue(action["val"]))
                case "echo":
                    print(fetchValue(action["val"]))
                case _: 
                    print("Unknown type", action["type"])
                    exit(1)


    def __runThread(self, task : Task):
        with self.__mutex:
            self.__currentlyRunning.append(task)
            self.__currentlyPending.remove(task)
        # run time left
        maxruntime = task["maxruntime"]
        if isinstance(maxruntime, str):
            maxruntime = eval(maxruntime)

        stopevent = threading.Event()
        threading.Timer(maxruntime, self.__stopThread, [task, stopevent]).start()
    
        print("Running task", task["name"])
        self.__handleActions(task.get("start", []))

        while not stopevent.is_set():
            time.sleep(0.5)

    def __stopThread(self, task : Task, stopevent : threading.Event):
        self.__handleActions(task.get("stop", []))
        stopevent.set()
        self.__currentlyRunning.remove(task)

    def block_till_done(self):
        while self.__scheduler.queue or self.__currentlyRunning:
            self.__scheduler.run(blocking=True)
        print("All tasks completed")
        
    def isRunning(self):
        return self.__currentlyRunning