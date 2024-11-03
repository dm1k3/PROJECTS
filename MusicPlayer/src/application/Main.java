package application;
	
import java.io.IOException;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.stage.Stage;
import javafx.scene.Parent;
import javafx.scene.Scene;


public class Main extends Application {
	
	@Override
	public void start(Stage stage) throws IOException {
		// загружаем файл, описывающий интерфейс приложения:
		Parent root = FXMLLoader.load(getClass().getResource("Scene.fxml"));
		// создаем новую сцену:
		Scene scene = new Scene(root);
		// устанавливаем запрет на изменение размера окна приложения:
		stage.setResizable(false);
		// устанавливаем сцену в главное окно:
		stage.setScene(scene);
		// отображаем главное окно на экране пользователя:
		stage.show();
	}
	
	public static void main(String[] args) {
		// запускаем приложение:
		launch(args);
	}
}
