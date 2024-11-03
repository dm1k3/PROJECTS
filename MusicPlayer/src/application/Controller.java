package application;

import java.io.File;
import java.io.FilenameFilter;
import java.net.URI;
import java.nio.file.Paths;

import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.Slider;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.AnchorPane;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.scene.media.MediaPlayer.Status;
import javafx.stage.DirectoryChooser;
import javafx.stage.FileChooser;
import javafx.util.Duration;



public class Controller {
	
	@FXML
	AnchorPane mainPane;
	@FXML
	Slider mySlider;
	@FXML
	Label startTimeLabel;
	@FXML
	Label endTimeLabel;
	@FXML
	Label songNameLabel;
	@FXML
	Button playButton;
	@FXML
	Button autoPlay;
	

	int songNumber = 0;
	File[] files;
	Media media;
	MediaPlayer mdPlayer;
	FileChooser fileChooser = new FileChooser();
	boolean isPlaying = false;
	boolean autoPlaying = false;
	Image pauseImage = new Image(getClass().getResourceAsStream("img/pause.png"));
	Image playImage = new Image(getClass().getResourceAsStream("img/play.png"));
	Image autoPlayImageOff = new Image(getClass().getResourceAsStream("img/repeat.png"));
	Image autoPlayImageOn = new Image(getClass().getResourceAsStream("img/repeatOn.png"));
	ImageView autoPlayOffImageView = new ImageView(autoPlayImageOff);
	ImageView autoPlayOnImageView = new ImageView(autoPlayImageOn);
	ImageView pauseImageView = new ImageView(pauseImage);
	ImageView playImageView = new ImageView(playImage);
	URI uri;
	
	public void playMedia() {
		/* Функция, срабатывающая при нажатии на кнопку "Запуск".*/
				
		// Проверяем, что плеер не проигрывается:
		if (!isPlaying) {
			try {
				// Запускаем проигрывание плеера:
				mdPlayer.play();
				// Ставим флаг отслеживания проигрывания:
				isPlaying = true;
				// Устанавливаем размеры изображения "Пауза":
				pauseImageView.setFitWidth(40);
				pauseImageView.setFitHeight(40);
				// Меняем изображение на изображение "Пауза":
				playButton.setGraphic(this.pauseImageView);
			}
			catch (NullPointerException e) {
				// Если плеер не может проиграть файл (файл не выбран):
				showWarningNoneFile();
			}
		} 
		else {
			// Приостанавливаем проигрывание плеера:
			mdPlayer.pause();
			// Ставим флаг для отслеживания проигрывания:
			isPlaying = false;
			// Устанавливаем размеры изображения "Запустить":
			playImageView.setFitWidth(40);
			playImageView.setFitHeight(40);
			// Меняем изображение на "Запустить":
			playButton.setGraphic(this.playImageView);
		}	
		
	}
	
	
	public void stopMedia() {
		/* Функция, срабатывающая при нажатии на кнопку "Стоп".*/
		
		try {
			// Останавливаем проигрывание плеера и сбрасываем в начало:
			mdPlayer.stop();
			// Устанавливаем флаг отслеживания проигрывания:
			isPlaying = false;
			// Устанавливаем размеры изображения "Запуск":
			playImageView.setFitWidth(40);
			playImageView.setFitHeight(40);
			// Устанавливаем изображение:
			playButton.setGraphic(playImageView);
		}
		catch (NullPointerException e) {
			// Выводим предупреждение (файл не выбран):
			showWarningNoneFile();
		}
	}
	
	
	public void nextSong() {
		/* Функция, срабатывающая при нажатии на кнопку "Следующая песня".*/
		
		// Проверяем, что очередь на воспроизведение существует:
		if (files != null) {
			// Если номер песни меньше длины очереди:
			if (songNumber < files.length - 1)
				// Увеличиваем номер песни на 1:
				songNumber++;
			else 
				// Устанавливаем номер песни на начальный:
				songNumber = 0;
			
			// Приостанавливаем проигрывание:
			stopMedia();
			// Передаем следующую песню для создания плеера:
			setMediaPlayer(this.files[songNumber]);
			// Запускаем проигрывание:
			playMedia();
		}
		else {
			// Если очередь пуста - выводим предупреждение:
			showWarningEmptyQueue();
		}
	}
	
	
	public void previousSong() {
		/* Функция, срабатывающая при нажатии на кнопку "Предыдущая песня".*/
		
		// Проверяем, что очередь существует:
		if (this.files != null) {
			// Если номер песни больше или 1 и не выходит за очередь:
			if (songNumber >= 1 && songNumber <= files.length - 1)
				// Уменьшаем номер песни:
				songNumber--;
			else 
				// Берем последнюю песню из очереди:
				songNumber = files.length - 1;
			
			// Сбрасываем плеер:
			stopMedia();
			
			// Передаем песню для создания плеера: 
			setMediaPlayer(files[songNumber]);
			// Запускаем проигрывание:
			playMedia();
		}
		else {
			// Выводим предупреждение, что очередь пуста:
			showWarningEmptyQueue();
		}
	}
	
	
	public void selectFile() {
		/* Функция, срабатывающая при нажатии на кнопку меню "Выбрать файл".*/
		
		// Проверяем, что плеер существует и находится в состояниях "Проигрывается" или "На паузе":
		if (mdPlayer != null && (mdPlayer.getStatus() == Status.PLAYING || mdPlayer.getStatus() == Status.PAUSED))
			// Если верно, то останавливаем плеер:
			stopMedia();
		// Устанавливаем фильтр, чтобы выбирать только 'mp3' файлы:
		fileChooser.getExtensionFilters().add(new FileChooser.ExtensionFilter("MP3 Files", "*.mp3"));
		// Выбираем файл:
		File selectedFile = fileChooser.showOpenDialog(mainPane.getScene().getWindow());
		// Передаем выбранный файл для создания плеера:
		setMediaPlayer(selectedFile);
	}
	
	public void setMediaPlayer(File selectedFile) {
		/* Функция создает медиаплеер.*/
		
		try {
			// Конвертируем путь файла в Uri:
			uri = Paths.get(selectedFile.getAbsolutePath()).toUri();
			// Устанавливаем название файла в лейбл:
			setSongNameLabel(selectedFile);
		} // Если файл не выбран - ничего не выводим:
		catch (NullPointerException e) {}
		// Создаем новый объект Media:
		media = new Media(uri.toString());
		// Если плеер уже существует:
		if (mdPlayer != null)
			// Удаляем плеер:
			mdPlayer.dispose();
		// Создаем новый плеер: 
		mdPlayer = new MediaPlayer(media);

		// Медиаплеер создан и готов к воспроизведению:
		mdPlayer.setOnReady(() -> {
			// Устанавливаем начальные значения слайдера:
			mySlider.setMin(0);
			// Шаг слайдера:
			mySlider.setBlockIncrement(1);
			// Устанавливаем конечное время песни в лейбл:
			setEndTimeLabel();
			// устанавливаем слушатель для слайдера, чтобы он двигался при проигрывании песни:
			setListenerDurationSlider();
			// Устанавливаем слушатель для слайдера, чтобы он перематывал песню:
			setListenerRewindSong();
		});
		
		// После завершения проигрывания:
		mdPlayer.setOnEndOfMedia(() -> {
			// Если включено автопроигрывание и существует очередь песен:
			if (autoPlaying && files != null) {
				// Включаем следующую песню:
				nextSong();
			}
			
		});
		
	}
	
	public void setEndTimeLabel() {
		/* Функция устанавливаем конечное время песни в лейбл.*/
		
		// Устанавливаем конечное значение для шага слайдера (конечное время песни): 
		mySlider.setMax(media.getDuration().toSeconds());
		// Получает конечное время песни:
		long endMinutes = (long) media.getDuration().toMinutes();
		long endSeconds = (long) media.getDuration().toSeconds() % 60;
		// Создаем формат строки для вывода в лейбл:
		String formattedEndTime = String.format("%d:%02d", endMinutes, endSeconds);
		// Устанавливаем в лейбл созданную строку: 
		endTimeLabel.setText(formattedEndTime);
	}
	
	public void setListenerDurationSlider() {
		/* Функция устанавливает слушатель для продвижения слайдера
		 * по ходу проигрывания песни.*/
		
		// Добавляем слушатель для продвижения слайдера при проигрывании песни;
		// currentTimeProperty - возвращает текущее время проигрывания плеера:
		mdPlayer.currentTimeProperty().addListener((obs, oldTime, newTime) -> {
			if (!mySlider.isValueChanging()) {
				// Устанавливаем новое значение слайдера: 
				mySlider.setValue(newTime.toSeconds());
				// Изменяем время проигрывания песни:
				long minutes = (long) newTime.toMinutes();
				long seconds = (long) newTime.toSeconds() % 60;
				String formattedTime = String.format("%d:%02d", minutes, seconds);
				// Устанавливаем созданную строку в лейбл: 
				startTimeLabel.setText(formattedTime);
			}
		});
	}
	
	public void setListenerRewindSong() {
		/* Функция устанавливает слушатель для перемотки песни через изменение слайдера.*/
		
		// Устанавливаем слушатель на изменение слайдера пользователем:
		mySlider.valueChangingProperty().addListener((obs, wasChanging, isChanging) -> {
			if (!isChanging && mdPlayer != null)
				// Устанавливаем новое время воспроизведения: 
				mdPlayer.seek(Duration.seconds(mySlider.getValue()));
		});
	}

	
	public void selectFolder() {
		/* Функция, срабатывающая при нажатии кнопки меню "Выбрать папку".*/
		
		// Проверяем, что плеер существует и находится в состояниях "Проигрывается" или "На паузе":
		if (mdPlayer != null && (mdPlayer.getStatus() == Status.PLAYING || mdPlayer.getStatus() == Status.PAUSED))
			// Останавливаем плеер:
			stopMedia();
		// Создаем объект для выбора директории с файлами:
		DirectoryChooser chooser = new DirectoryChooser();
		// Устанавливаем название окна выбора директории:
		chooser.setTitle("Выберите папку с файлами mp3:");
		// Получаем выбранную директорию:
		File selectedFolder = chooser.showDialog(mainPane.getScene().getWindow());
		// Если директория выбрана:
		if (selectedFolder != null) {
			// Получаем все файлы в директории и устанавливаем фильтр на выбор только файлов-mp3:
			files = selectedFolder.listFiles(new FilenameFilter() {
				@Override
				public boolean accept(File dir, String name) {
					// Файл заканчивается на ".mp3":
					return name.endsWith(".mp3");
				}
				
			});
			// Если файлы есть:
			if (files != null) {
				// передаем файл по номеру песни:
				setMediaPlayer(files[songNumber]);
			}
		}
	}
	
	public void setSongNameLabel(File file) {
		/* Функция устанавливает название файла в лейбл.*/
		
		try {
			// Получаем имя файла:
			String name = file.getName();
			// Устанавливаем имя файла в лейбл:
			songNameLabel.setText(name);
		} // Если пользователь не выбрал файл - ничего не делаем:
		catch (NullPointerException e) {}
	}
	
	
	public void setAutoPlay() {
		/* Функция включает или выключает функцию автовоспроизведения.*/
		
		// Если очередь файлов не пуста:
		if (files != null)
			// И если автопроигрывание включено:
			if (autoPlaying) {
				// Меняем флаг для отслеживания автопроигрывания:
				autoPlaying = false;
				// Меняем изображение на "Автопроигрывание выключено";
				// устанавливаем размеры изображения:
				autoPlayOffImageView.setFitWidth(40);
				autoPlayOffImageView.setFitHeight(40);
				// Устанавливаем изображение:
				autoPlay.setGraphic(autoPlayOffImageView);
			} // Если проигрывание выключено:
			else {
				// Меняем флаг для отслеживания автопроигрывания:
				autoPlaying = true;
				// Меняем изображение на "Автопроигрывание включено";
				// устанавливаем размеры изображения:
				autoPlayOnImageView.setFitWidth(40);
				autoPlayOnImageView.setFitHeight(40);
				// Устанавливаем изображение:
				autoPlay.setGraphic(autoPlayOnImageView);
			}
		else
			// Выводим предупреждение, что очередь песен пуста:
			showWarningEmptyQueue();
	}
	
	
	public void clearSongs() {
		/*Функция очищает очередь песен.*/
		
		// Если очередь песен не пуста:
		if (files != null) { 
			// Чистим очередь песен:
			files = null;
			// Если автопроигрывание включено - выключаем:
			if (autoPlaying) {
				// Меняем флаг отслеживания автопроигрывания:
				autoPlaying = false;
				// Устанавливаем размеры изображения "Автопроигрывание выключено":
				autoPlayOffImageView.setFitWidth(40);
				autoPlayOffImageView.setFitHeight(40);
				// Устанавливаем изображение:
				autoPlay.setGraphic(autoPlayOffImageView);
			}
		}
		else {
			// Выводим предупреждение - очередь пуста:
			showWarningEmptyQueue();
		}
	}
	
			
	public void showWarningNoneFile() {
		/*Функция создает и выводит окно с предупреждением "Файл не выбран!".*/
		
		// Создаем окно предупреждения:
		Alert alert = new Alert(AlertType.WARNING);
		// Устанавливаем название окна:
		alert.setTitle("Предупреждение");
		// Устанавливаем заголовок текста:
		alert.setHeaderText("ФАЙЛ НЕ ВЫБРАН !");
		// Устанавливаем текст предупреждения:
		alert.setContentText("Сначала выберите аудио файл !!!");
		// Показываем окно:
		alert.showAndWait();
	}
	
	public void showWarningEmptyQueue() {
		/*Функция создает и выводит окно с предупреждением "Очередь песен пуста!".*/
		
		// Создаем окно предупреждения:
		Alert alert = new Alert(AlertType.WARNING);
		// Устанавливаем название окна:
		alert.setTitle("Предупреждение");
		// Устанавливаем заголовок текста:
		alert.setHeaderText("ОЧЕРЕДЬ ПЕСЕН ПУСТА !");
		// Устанавливаем текст предупреждения:
		alert.setContentText("Выберите папку с файлами !!!");
		// Показываем окно:
		alert.showAndWait();
	}
}
