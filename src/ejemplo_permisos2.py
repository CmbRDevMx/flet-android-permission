import flet as ft
import os
import platform
from datetime import datetime

class VideoApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Video Explorer"
        self.page.theme_mode = ft.ThemeMode.SYSTEM
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        
        # Inicializar el manejador de permisos
        self.permission_handler = ft.PermissionHandler()
        self.page.overlay.append(self.permission_handler)
        
        # Contenedor para mostrar videos
        self.videos_grid = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=200,
            spacing=10,
            run_spacing=10,
            padding=20,
        )
        
        # Estado de la aplicación
        self.permission_status = "Desconocido"
        self.status_text = ft.Text(
            f"Estado del permiso: {self.permission_status}",
            size=16,
            weight=ft.FontWeight.BOLD
        )
        
        # Crear la interfaz de usuario
        self.initialize_ui()
        
        # Verificar permisos al inicio
        self.check_video_permission(None)
    
    def initialize_ui(self):
        # AppBar
        self.page.appbar = ft.AppBar(
            title=ft.Text("Explorador de Videos"),
            center_title=True,
            bgcolor=ft.colors.BLUE_700,
            actions=[
                ft.IconButton(
                    icon=ft.icons.SETTINGS,
                    tooltip="Abrir configuración",
                    on_click=self.open_app_settings
                )
            ]
        )
        
        # Botones de acción de permisos
        permission_controls = ft.Row(
            controls=[
                ft.ElevatedButton(
                    "Verificar permiso",
                    icon=ft.icons.CHECK_CIRCLE,
                    on_click=self.check_video_permission
                ),
                ft.ElevatedButton(
                    "Solicitar permiso",
                    icon=ft.icons.VIDEO_LIBRARY,
                    on_click=self.request_video_permission
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        # Botón para simular carga de videos
        load_button = ft.ElevatedButton(
            "Cargar videos",
            icon=ft.icons.REFRESH,
            on_click=self.load_sample_videos
        )
        
        # Estructura principal
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        self.status_text,
                        permission_controls,
                        load_button,
                        ft.Divider(),
                        ft.Text("Videos encontrados:", size=16),
                        self.videos_grid
                    ],
                    spacing=20,
                    scroll=ft.ScrollMode.AUTO
                ),
                padding=20,
                expand=True
            )
        )
    
    def check_video_permission(self, e):
        # Verificar permiso de videos
        result = self.permission_handler.check_permission(ft.PermissionType.VIDEOS)
        self.permission_status = "Concedido" if result else "Denegado"
        self.status_text.value = f"Estado del permiso: {self.permission_status}"
        
        # Mostrar snackbar con resultado
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Permiso de videos: {self.permission_status}"),
            action="OK"
        )
        self.page.snack_bar.open = True
        
        # Actualizar UI
        self.page.update()
    
    def request_video_permission(self, e):
        # Solicitar permiso
        result = self.permission_handler.request_permission(ft.PermissionType.VIDEOS)
        
        # Actualizar estado
        self.check_video_permission(None)
    
    def open_app_settings(self, e):
        # Abrir configuración de la app
        self.permission_handler.open_app_settings()
        
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Abriendo configuración de la aplicación"),
            action="OK"
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def load_sample_videos(self, e):
        # Primero verificar el permiso
        result = self.permission_handler.check_permission(ft.PermissionType.VIDEOS)
        
        if not result:
            # Si no tenemos permiso, solicitar
            self.page.dialog = ft.AlertDialog(
                title=ft.Text("Permiso requerido"),
                content=ft.Text("Se necesita permiso para acceder a los videos."),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda _: self.close_dialog()),
                    ft.TextButton("Solicitar permiso", on_click=self.handle_permission_dialog)
                ]
            )
            self.page.dialog.open = True
            self.page.update()
            return
        
        # Limpiar grid
        self.videos_grid.controls.clear()
        
        # Datos de ejemplo para simular videos
        sample_videos = [
            {"name": "Video familiar", "date": "2025-04-28", "duration": "2:45"},
            {"name": "Viaje a la playa", "date": "2025-04-20", "duration": "5:12"},
            {"name": "Cumpleaños", "date": "2025-03-15", "duration": "10:30"},
            {"name": "Conferencia", "date": "2025-02-10", "duration": "45:22"},
            {"name": "Recital escolar", "date": "2025-01-05", "duration": "15:10"},
            {"name": "Reunión familiar", "date": "2024-12-25", "duration": "30:45"},
        ]
        
        # Agregar videos a la cuadrícula
        for video in sample_videos:
            self.videos_grid.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Icon(
                                        ft.icons.VIDEO_FILE,
                                        size=50,
                                        color=ft.colors.BLUE_400
                                    ),
                                    padding=10,
                                    alignment=ft.alignment.center
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                video["name"],
                                                size=14,
                                                weight=ft.FontWeight.BOLD
                                            ),
                                            ft.Text(
                                                f"Fecha: {video['date']}",
                                                size=12
                                            ),
                                            ft.Text(
                                                f"Duración: {video['duration']}",
                                                size=12
                                            )
                                        ],
                                        spacing=5
                                    ),
                                    padding=10
                                )
                            ]
                        ),
                        padding=5
                    )
                )
            )
        
        # Actualizar UI
        self.page.update()
    
    def handle_permission_dialog(self, e):
        # Cerrar diálogo
        self.close_dialog()
        # Solicitar permiso
        self.request_video_permission(None)
    
    def close_dialog(self, e=None):
        self.page.dialog.open = False
        self.page.update()

def main(page: ft.Page):
    app = VideoApp(page)

# Punto de entrada para ejecutar la aplicación
if __name__ == "__main__":
    ft.app(target=main)
