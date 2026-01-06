import flet as ft
import requests

def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.bgcolor = ft.Colors.GREY_100

    #地域リスト取得
    area_data = requests.get(
        "http://www.jma.go.jp/bosai/common/const/area.json"
    ).json()
    offices = area_data["offices"]

    #結果表示用コンテナ
    result = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
    )

    result.controls.append(
        ft.Text(
            "左の地域を選択してください",
            size=16,
            color=ft.Colors.GREY_700
        )
    )

    #天気取得関数
    def show_weather(area_code, area_name):
        url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
        data = requests.get(url).json()

        series = data[0]["timeSeries"][0]
        dates = series["timeDefines"]
        weathers = series["areas"][0]["weathers"]

        result.controls.clear()
        result.controls.append(
            ft.Text(
                f"{area_name} の天気予報（最大7日）",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK,
                text_align=ft.TextAlign.CENTER
            )
        )

        for i in range(min(7, len(dates))):
            from datetime import datetime
            raw_date = dates[i][:10]
            dt = datetime.strptime(raw_date, "%Y-%m-%d")
            date_str = f"{dt.year}年{dt.month}月{dt.day}日"
            weather = weathers[i].replace("　", " ")
            result.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(date_str, size=12, color=ft.Colors.BLACK),
                            ft.Text(weather, size=14, color=ft.Colors.BLACK),
                        ],
                        spacing=4,
                    ),
                    padding=10,
                    margin=ft.margin.only(bottom=8),
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=10,
                )
            )

        page.update()

    #地域リストタイル作成
    tiles = []
    for code, info in offices.items():
        tiles.append(
            ft.ListTile(
                title=ft.Text(info["name"], size=14, color=ft.Colors.BLACK),
                dense=True,
                on_click=lambda e, c=code, n=info["name"]: show_weather(c, n)
            )
        )

    page.add(
        ft.Row(
            [
                ft.Container(
                    content=ft.ListView(tiles, expand=True),
                    width=280,
                    border=ft.border.all(1, ft.Colors.BLACK12),
                    padding=10,
                    bgcolor=ft.Colors.GREY_50
                ),
                ft.Container(
                    content=result,
                    expand=True,
                    border=ft.border.all(1, ft.Colors.BLACK12),
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12
                )
            ],
            expand=True
        )
    )

ft.app(target=main)
