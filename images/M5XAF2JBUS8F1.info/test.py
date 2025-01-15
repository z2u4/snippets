

import datetime
from autoplayer.player import AutoPlayer


w = AutoPlayer(
    "test.toml", overwriteCurrentTime=datetime.time(14, 1, 0)
).block_till_done()