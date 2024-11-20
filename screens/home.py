from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from datetime import datetime, timedelta
import calendar


class CustomCalendar(GridLayout):
    def __init__(self, view_mode='month', on_date_change=None, **kwargs):
        super(CustomCalendar, self).__init__(**kwargs)
        self.view_mode = view_mode  # Define el modo inicial
        self.current_date = datetime.now()  # Fecha base para navegar
        self.on_date_change = on_date_change  # Callback para actualizar el título
        self.spacing = 2
        self.padding = 5
        self.update_view()

    def update_view(self):
        """Actualizar la vista según el modo seleccionado."""
        self.clear_widgets()

        # Llamar al callback para actualizar el título (si está definido)
        if self.on_date_change:
            self.on_date_change(self.current_date)

        if self.view_mode == 'month':
            self.create_month_view()
        elif self.view_mode == 'week':
            self.create_week_view()
        elif self.view_mode == 'day':
            self.create_day_view()

    def create_month_view(self):
        """Crea la vista del calendario mensual."""
        self.cols = 7

        # Crear encabezados de días
        days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        for day in days:
            self.add_widget(Label(text=day, bold=True, size_hint_y=None, height=40))

        # Obtener el calendario del mes actual
        year, month = self.current_date.year, self.current_date.month
        cal = calendar.monthcalendar(year, month)

        for week in cal:
            for day in week:
                if day == 0:
                    # Día vacío
                    self.add_widget(Label(text=''))
                else:
                    btn = Button(
                        text=str(day),
                        background_normal='',
                        background_color=(0.9, 0.9, 0.9, 1),
                        color=(0, 0, 0, 1)
                    )
                    btn.bind(on_press=lambda x, day=day: self.on_day_select(day))
                    self.add_widget(btn)

    def create_week_view(self):
        """Crea la vista del calendario semanal."""
        self.cols = 7

        # Calcular inicio de la semana
        start_of_week = self.current_date - timedelta(days=self.current_date.weekday())
        days_of_week = [(start_of_week + timedelta(days=i)) for i in range(7)]

        for day in days_of_week:
            btn = Button(
                text=day.strftime('%d/%m'),
                background_normal='',
                background_color=(0.9, 0.9, 0.9, 1),
                color=(0, 0, 0, 1)
            )
            btn.bind(on_press=lambda x, day=day: self.on_day_select(day.day))
            self.add_widget(btn)

    def create_day_view(self):
        """Crea la vista del calendario diario."""
        self.cols = 1

        # Mostrar solo el día actual
        btn = Button(
            text=self.current_date.strftime('%d/%m/%Y'),
            background_normal='',
            background_color=(0.9, 0.9, 0.9, 1),
            color=(0, 0, 0, 1)
        )
        btn.bind(on_press=lambda x: self.on_day_select(self.current_date.day))
        self.add_widget(btn)

    def on_day_select(self, day):
        selected_date = datetime(self.current_date.year, self.current_date.month, day)
        print(f'Fecha seleccionada: {selected_date.strftime("%d/%m/%Y")}')
        # Navigate to video screen
        self.parent.parent.parent.current = 'video'

    def navigate(self, direction):
        """Navegar según el modo de vista."""
        if self.view_mode == 'month':
            self.navigate_month(direction)
        elif self.view_mode == 'week':
            self.navigate_week(direction)
        elif self.view_mode == 'day':
            self.navigate_day(direction)

    def navigate_month(self, direction):
        """Navegar entre meses."""
        if direction == 'previous':
            # Mes anterior
            self.current_date = self.current_date.replace(day=1) - timedelta(days=1)
        elif direction == 'next':
            # Mes siguiente
            next_month = self.current_date.replace(day=28) + timedelta(days=4)
            self.current_date = next_month.replace(day=1)
        self.update_view()

    def navigate_week(self, direction):
        """Navegar entre semanas."""
        if direction == 'previous':
            # Mes anterior
            self.current_date -= timedelta(weeks=1)
        elif direction == 'next':
            # Mes siguiente
            self.current_date += timedelta(weeks=1)
        self.update_view()

    def navigate_day(self, direction):
        """Navegar entre días."""
        if direction == 'previous':
            # Día anterior
            self.current_date -= timedelta(days=1)
        elif direction == 'next':
            # Día siguiente
            self.current_date += timedelta(days=1)
        self.update_view()


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        # Layout principal
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Fondo del screen
        with self.canvas.before:
            Color(rgba=(176 / 255, 198 / 255, 206 / 255, 1))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Título que muestra el mes y el año
        self.title_label = Label(
            text='',
            font_size=24,
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.title_label)

        # Navbar para cambiar vistas
        self.navbar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.navbar.add_widget(Button(text='Mes', on_press=self.switch_to_month))
        self.navbar.add_widget(Button(text='Semana', on_press=self.switch_to_week))
        self.navbar.add_widget(Button(text='Día', on_press=self.switch_to_day))
        self.layout.add_widget(self.navbar)

        # Barra de navegación del calendario
        self.navigation_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.navigation_bar.add_widget(Button(text='Anterior', on_press=self.navigate_previous))
        self.navigation_bar.add_widget(Button(text='Siguiente', on_press=self.navigate_next))
        self.layout.add_widget(self.navigation_bar)

        # Instancia del calendario
        self.calendar = CustomCalendar(view_mode='month', on_date_change=self.update_title, size_hint=(1, 0.7))
        self.layout.add_widget(self.calendar)

        # Selected date label
        self.selected_date_label = Label(
            text='Seleccione una fecha',
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.selected_date_label)

        # Agregar layout a la pantalla
        self.add_widget(self.layout)

    def switch_to_month(self, instance):
        self.calendar.view_mode = 'month'
        self.calendar.update_view()

    def switch_to_week(self, instance):
        self.calendar.view_mode = 'week'
        self.calendar.update_view()

    def switch_to_day(self, instance):
        self.calendar.view_mode = 'day'
        self.calendar.update_view()

    def update_title(self, current_date):
        """Actualizar el título con el mes y el año actuales."""
        # Nombre del mes
        month_name = current_date.strftime('%B')
        year = current_date.year
        self.title_label.text = f'{month_name} {year}'

    def navigate_previous(self, instance):
        self.calendar.navigate('previous')

    def navigate_next(self, instance):
        self.calendar.navigate('next')

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos
