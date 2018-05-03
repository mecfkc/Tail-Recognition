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

public class PrintTrap extends Application{
	@Override
	public void start(Stage primaryStage){
		StackPane root = new StackPane();
		primaryStage.setMaxHeight(300);
        primaryStage.setMaxWidth(500);
        primaryStage.setResizable(false);
        Scene scene = new Scene(root, primaryStage.getMaxWidth(), primaryStage.getMaxHeight());
        WritableImage wim = new WritableImage(500, 300);

        Canvas canvas = new Canvas(500, 300);
         int iteration = 0;
        while (iteration < 100){
        GraphicsContext gc = canvas.getGraphicsContext2D();
        drawShapes(gc);
        canvas.snapshot(null, wim);
        root.getChildren().add(canvas);

        String filename = "ytr" + iteration + ".png";
		File file = new File(filename);
        try {
            ImageIO.write(SwingFXUtils.fromFXImage(wim, null), "png", file);
        	} catch (Exception s) {
        }
        root.getChildren().clear();
        iteration++;
    }

	}

	public static void main(String[] args) {
    	launch(args);
	}

	private void drawShapes (GraphicsContext gc) {
		Random random = new Random();
    int randvalue = random.nextInt(200);
		int randscale = random.nextInt(200)+50;
		gc.setFill(Color.WHITE);
		gc.fillRect(0, 0, 500, 300);
		gc.setFill(Color.YELLOW);
    gc.fillRect((240.2-randvalue), (0.0+randvalue), 21*(randscale+100)/100 , 133.3*(randscale+100)/100);
	}

	public Paint randomColor() {
        Random random = new Random();
        int r = random.nextInt(255);
        int g = random.nextInt(255);
        int b = random.nextInt(255);
        return Color.rgb(r, g, b);
	}

}
