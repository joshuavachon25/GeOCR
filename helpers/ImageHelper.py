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
        frame.img.image = imgtk
        f_w = frame.winfo_width()
        f_h = frame.winfo_height()
        print(f_w)
        frame.img.create_image(f_w/2, f_h/2, anchor='center', image=imgtk)
        frame.w = w
        frame.h = h
