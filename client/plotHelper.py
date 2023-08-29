import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import num2date, drange
from matplotlib.widgets import RectangleSelector, Button
from matplotlib.transforms import Bbox

def create_plot(x,y, title):
    input_x = x.copy()
    input_y = y.copy()

    # Tworzenie wykresu
    fig, ax = plt.subplots()
    line, = ax.plot(x, y, label='Median Price of Sail', linewidth=0.8)
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.set_title(title)
    ax.legend()
    info_text = ax.text(0.05, 0.9, '', transform=ax.transAxes, va='top')

    # Dodanie interaktywności za pomocą mplcursors
    def cursor_function(event):
        if event.inaxes:
            x_val = event.xdata
            y_val = event.ydata
            info_text.set_text(f'Time: {x_val:.2f} \nPrice: {y_val:.2f}')
            info_text.set_visible(True)
            ax.figure.canvas.draw()
    cursor = fig.canvas.mpl_connect('motion_notify_event', cursor_function)

    # Ustawienie zakresu osi Y dla początkowej perspektywy
    initial_ylim = ax.get_ylim()

    def on_xlims_change(axes):
        # Aktualizacja zakresu osi Y w zależności od zakresu osi X

        # ax.set_ylim(initial_ylim[0] * (axes.viewLim.width / (x[-1] - x[0])),
        #             initial_ylim[1] * (axes.viewLim.width / (x[-1] - x[0])))

        ax.set_ylim(initial_ylim[0] * (axes.viewLim.width / (x[-1] - x[0])),
                    initial_ylim[1] * (axes.viewLim.width / (x[-1] - x[0])))
        fig.canvas.draw_idle()


        # new_xlim = ax.get_xlim()
        # new_x = num2date(new_xlim[0]), num2date(new_xlim[1])
        #
        # # Aktualizacja zakresu osi Y w zależności od zakresu osi X
        # visible_indices = np.where((x >= new_x[0]) & (x <= new_x[1]))[0]
        # y_visible = y[visible_indices]
        #
        # ax.set_ylim(y_visible.min(), y_visible.max())
        # fig.canvas.draw_idle()

    # Przypisanie funkcji do zdarzenia zmiany zakresu osi X
    ax.callbacks.connect('xlim_changed', on_xlims_change)

    # Inicjalizacja prostokąta i bbox
    rect = plt.Rectangle((0, 0), 0, 0, fill=False, color='red', visible=False)
    ax.add_patch(rect)
    bbox = None

    # Funkcja do obsługi zaznaczania obszaru
    def on_rect_select(eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        rect.set_width(x2 - x1)
        rect.set_height(y2 - y1)
        rect.set_xy((x1, y1))
        rect.set_visible(True)
        global bbox
        bbox = Bbox.from_extents(x1, y1, x2, y2)

    # Przypisanie funkcji do rysowania prostokąta
    rs = RectangleSelector(ax, on_rect_select)

    # Funkcja do obsługi puszczenia klawisza myszy
    def on_release(event):
        global bbox
        if bbox is not None:
            rect.set_visible(False)
            ax.set_xlim(bbox.x0, bbox.x1)
            ax.set_ylim(bbox.y0, bbox.y1)
            ax.figure.canvas.draw()

    # Przypisanie funkcji do puszczenia klawisza myszy
    fig.canvas.mpl_connect('button_release_event', on_release)

    # Funkcja przywracająca pierwotny wykres
    def reset_plot(event):
        ax.set_xlim(min(input_x), max(input_x))
        ax.set_ylim(min(input_y), max(input_y))
        ax.figure.canvas.draw()

    # Dodanie przycisku
    reset_button_ax = plt.axes([0.85, 0.05, 0.1, 0.04])
    reset_button = Button(reset_button_ax, 'Reset', color='lightgoldenrodyellow', hovercolor='0.975')
    reset_button.on_clicked(reset_plot)

    plt.show()


def create_plots(x1, y1, y2, title):
    # Tworzenie wykresu
    fig, ax = plt.subplots()
    line1, = ax.plot(x1, y1, label='Dataset 1', linewidth=0.8)
    line2, = ax.plot(x1, y2, label='Dataset 2', linewidth=0.8)
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.set_title(title)
    ax.legend()
    info_text = ax.text(0.05, 0.9, '', transform=ax.transAxes, va='top')

    # Dodanie interaktywności za pomocą mplcursors
    def cursor_function(event):
        if event.inaxes:
            x_val = event.xdata
            y_val = event.ydata
            info_text.set_text(f'Time: {x_val:.2f} \nPrice: {y_val:.2f}')
            info_text.set_visible(True)
            ax.figure.canvas.draw()
    cursor = fig.canvas.mpl_connect('motion_notify_event', cursor_function)

    plt.show()