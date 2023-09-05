from PIL import Image, ImageTk


def show_preview(frame, path, mode='img'):
    image = Image.open(path)
    set_image(frame, image, path, mode)


def get_preview_size(frame, image):
    frame.update()
    if image.width > image.height:
        w = int(frame.winfo_width())
        h = int((image.height / image.width ) * w)
    else:
        h = int(frame.winfo_height())
        w = int((image.width / image.height) * h)
    print(frame.winfo_width(), frame.winfo_height(), w, h)
    return w, h


def set_image(frame, image, path, mode):
    (w, h) = get_preview_size(frame, image)
    img = image.resize((w, h), Image.LANCZOS)
    imgtk = ImageTk.PhotoImage(img)
    if mode == 'img':
        frame.img.configure(image=imgtk)
        frame.img.image = imgtk
    else:
        frame.canvas.image = imgtk
        f_w = frame.winfo_width()
        f_h = frame.winfo_height()
        frame.canvas.create_image(0, 0, anchor='nw', image=imgtk)
        frame.w = w
        frame.h = h
