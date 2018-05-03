//Programmed by Christian Upschulte - Underwater Robotics 2018
//PrintTri.java
//Tool to output a specified number of png files of triangles
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.layout.BorderPane;
import javafx.scene.paint.Color;
import javafx.scene.paint.Paint;
import javafx.scene.shape.*;
import javafx.stage.Stage;
import java.io.File;
import javafx.scene.Node.*;
import java.io.IOException;
import javafx.embed.swing.SwingFXUtils;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javax.imageio.ImageIO;
import java.util.Random;
import javafx.scene.layout.StackPane;
import javafx.scene.image.WritableImage;

/* How to compile:
    In terminal, open the directory, run the command 'javac PrintTri.java'
    That creates the class files
    Then we use 'java PrintTri' to run the class file and the program
*/


public class PrintTri extends Application{ //main class
	@Override
	public void start(Stage primaryStage){
        //create a stack pane to hold objects
		StackPane root = new StackPane();

        //set the dimensions of the stage
		primaryStage.setMaxHeight(300);
        primaryStage.setMaxWidth(500);
        primaryStage.setResizable(false);

        //set the dimensitons of the scene
        Scene scene = new Scene(root, primaryStage.getMaxWidth(), primaryStage.getMaxHeight());
        //create a canvas and writable image
        WritableImage wim = new WritableImage(500, 300);
        Canvas canvas = new Canvas(500, 300);

        int numfiles = 100; //the number of png files you want to output
        int iteration =0; //counter for loop

        while (iteration < numfiles){
            //add graphics to the canvas
            GraphicsContext gc = canvas.getGraphicsContext2D();

            //create a drawing
            drawShapes(gc);
            canvas.snapshot(null, wim);

            //add canvas to stack pane
            root.getChildren().add(canvas);

            //this will name each file uniquely
            String filename = "yt" + iteration + ".png";
		    File file = new File(filename);
            //try writing to file
            try {
               ImageIO.write(SwingFXUtils.fromFXImage(wim, null), "png", file);
        	} catch (Exception s) {
        }
        //clear root in order to add these things again with no error
        root.getChildren().clear();
        iteration++;
    }

	}
    //launch the application
	public static void main(String[] args) {
    	launch(args);
	}

    //drawshapes function
	private void drawShapes (GraphicsContext gc) {
		Random random = new Random(); //declare a random
			int scale = random.nextInt(200);
    	int randvalue = scale+150; //random scaling int
        int xrand = random.nextInt(350); //random x position int
        int yrand = random.nextInt(100); //random y position int
		gc.setFill(Color.WHITE); //set the first fill, background color
		gc.fillRect(0, 0, 500, 300);//create a rectangle background
		gc.setFill(Color.WHITE); //set fill for outer triangle
		double xpoints[] = {(0.0+xrand), (0.0+xrand), (60.9+randvalue+xrand)};//create a group of xpoints for triangle
    	double ypoints[] = {(300.0-yrand), (200.0-randvalue-yrand), (300.0-yrand)}; //ypoints
    	int npoints = 3; //number of points for fillPolygon function
    	double xpoints2[] = {(0.0+xrand), (0.0+xrand), (29.2+xrand+(randvalue*(12.0/25.0)))};
    	double ypoints2[] = {(300.0-yrand), (-yrand+251.2-(randvalue*(20.0/41.0))), (300.0-yrand)};
		gc.fillPolygon(xpoints, ypoints, npoints); //create the first triangle
		gc.setFill(Color.YELLOW); //fill color for triangle two
		gc.fillPolygon(xpoints2, ypoints2, npoints); //create the second triangle
	}
    //returns a random rgb complex color
	public Paint randomColor() {
        Random random = new Random();
        int r = random.nextInt(255);
        int g = random.nextInt(255);
        int b = random.nextInt(255);
        return Color.rgb(r, g, b);
	}

}
