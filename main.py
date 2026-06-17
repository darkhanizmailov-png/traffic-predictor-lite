
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import tflite_runtime.interpreter as tflite

FEATURES_NAMES = [
    "average_speed_kmh","occupancy_rate","car_count","motorcycle_count",
    "truck_count","bus_count","is_holiday","temperature_c","humidity_pct",
    "precipitation_mm","wind_speed_kmh","visibility_km","air_quality_index",
    "uv_index","pressure_hpa","hour_sin","hour_cos"
]

class SimpleTrafficApp(App):
    def build(self):
        self.title = "Traffic Predictor Lite"
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Инструкция
        layout.add_widget(Label(
            text="Введите 17 признаков через запятую:",
            size_hint_y=None, height=30))
        
        # Поле ввода
        self.input_field = TextInput(
            hint_text="av_speed,occ,car,moto,truck,bus,holiday,temp,hum,prec,wind,vis,aqi,uv,press,h_sin,h_cos",
            multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.input_field)
        
        # Кнопка
        btn = Button(text="Предсказать", size_hint_y=None, height=50)
        btn.bind(on_press=self.predict)
        layout.add_widget(btn)
        
        # Результат
        self.result_label = Label(text="Ожидание...", size_hint_y=None, height=40)
        layout.add_widget(self.result_label)
        
        # Загрузка модели
        self.interpreter = tflite.Interpreter(model_path="traffic_lstm.tflite")
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.result_label.text = "Модель загружена (12x17)"
        
        return layout

    def predict(self, instance):
        try:
            raw = self.input_field.text.strip()
            vals = [float(x) for x in raw.split(",")]
            if len(vals) != 17:
                self.result_label.text = f"Нужно 17 чисел, введено {len(vals)}"
                return
            
            # Формируем последовательность 12x17
            seq = np.tile(np.array(vals, dtype=np.float32), (12, 1))
            seq = np.expand_dims(seq, axis=0)  # (1, 12, 17)
            
            self.interpreter.set_tensor(self.input_details[0]['index'], seq)
            self.interpreter.invoke()
            pred = self.interpreter.get_tensor(self.output_details[0]['index'])[0][0]
            self.result_label.text = f"Прогноз трафика: {pred:.2f} машин/час"
        except Exception as e:
            self.result_label.text = f"Ошибка: {str(e)}"

if __name__ == "__main__":
    SimpleTrafficApp().run()
