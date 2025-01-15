import java.awt.*;
import java.awt.event.*;
import java.awt.TrayIcon.MessageType;
import java.net.MalformedURLException;

class Sandbox {
    
    /**
     * Parsing a JSONObject string
     * 
     * @param args 
     */
    public static void main(String[] args) {
        Sandbox app = new Sandbox();
    }
    
    public Sandbox(){
        Frame f = new Frame("Button Example");  
        Button btn = new Button("Click Here");  
        btn.setBounds(50,100,80,30);  
        f.add(btn);  
        f.setSize(400,400);  
        f.setLayout(null);  
        f.setVisible(true);
        
        Sandbox _this = this;
        
        btn.addActionListener(new ActionListener()
        {
            @Override
            public void actionPerformed(ActionEvent e)
            {
                if (SystemTray.isSupported()) {
                    try{
                        _this.displayTray();
                    }catch(AWTException ex){
                        
                    }catch(MalformedURLException ex){
                    
                    }
                } else {
                    System.err.println("System tray not supported!");
                }
            }
        });
    }
    
    public void displayTray() throws AWTException, MalformedURLException {
        //Obtain only one instance 		of the SystemTray object
        SystemTray tray = SystemTray.getSystemTray();

        //If the icon is a file
        Image image = Toolkit.getDefaultToolkit().createImage("icon.png");
        //Alternative (if the icon is on the classpath):
        //Image image = Toolkit.getDefaultToolkit().createImage(getClass().getResource("icon.png"));

        TrayIcon trayIcon = new TrayIcon(image, "Java AWT Tray Demo");
        //Let the system resize the image if needed
        trayIcon.setImageAutoSize(true);
        //Set tooltip text for the tray icon
        trayIcon.setToolTip("System tray icon demo");
        tray.add(trayIcon);

        trayIcon.displayMessage("Hello, World", "Java Notification Demo", MessageType.INFO);
    }
}