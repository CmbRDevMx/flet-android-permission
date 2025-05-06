import flet as ft
import os

def main(page: ft.Page):
    page.title = "Videos en Descargas"
    page.scroll = ft.ScrollMode.ADAPTIVE

    ph = ft.PermissionHandler()
    page.overlay.append(ph)

    info = ft.Text("Estado: Esperando acción...")
    lista_videos = ft.ListView(expand=True)

    def check_storage_permission():
        try:
            granted = ph.check_permission(ft.PermissionType.STORAGE)
            info.value = f"Permiso de almacenamiento: {'Concedido' if granted else 'Denegado'}"
            page.update()
            return granted
        except Exception as e:
            info.value = f"Error: {e}"
            page.update()
            return False

    def open_app_settings(e):
        try:
            result = ph.open_app_settings()
            info.value = f"Abrir ajustes de la app: {result}"
            page.update()
        except Exception as e:
            info.value = f"Error al abrir ajustes: {e}"
            page.update()

    def buscar_videos(e):
        if not check_storage_permission():
            info.value = "Permiso requerido para acceder a archivos"
            page.update()
            return

        ruta = "/storage/emulated/0/Download"
        lista_videos.controls.clear()

        if not os.path.exists(ruta):
            info.value = "Ruta no existe o no es accesible"
            page.update()
            return

        videos = [f for f in os.listdir(ruta) if f.lower().endswith((".mp4", ".mkv", ".avi", ".mov", ".webm"))]
        
        if not videos:
            lista_videos.controls.append(ft.Text("No se encontraron videos en Descargas"))
        else:
            for video in videos:
                lista_videos.controls.append(ft.Text(video))

        page.update()

    page.add(
        ft.Text("Visor de Videos (Descargas)", size=20, weight=ft.FontWeight.BOLD),
        ft.ElevatedButton("Abrir ajustes de permisos", on_click=open_app_settings),
        ft.ElevatedButton("Buscar videos", on_click=buscar_videos),
        info,
        ft.Divider(),
        lista_videos
    )

    check_storage_permission()

ft.app(target=main)
