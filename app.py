import streamlit as st
from PIL import Image
import io

# Function to convert encoding data into 8-bit binary form using ASCII value of characters


def genData(data):
    newd = [format(ord(i), '08b') for i in data]
    return newd

# Function to modify pixels according to the 8-bit binary data and return them


def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        for j in range(8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1

        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if pix[-1] != 0:
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

# Function to encode data into an image


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

# Function to encode data into an image


def encode(img, data):
    image = Image.open(img)
    newimg = image.copy()
    encode_enc(newimg, data)
    return newimg

# Function to decode data from an image


def decode(img):
    image = Image.open(img)
    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data


# Streamlit UI
st.title("🔒 Image Steganography")
st.write("Hide and reveal secret messages in images with ease.")

st.sidebar.title("Select Action:")
choice = st.sidebar.radio(
    "Choose to encode or decode a message:", ("Encode a Message", "Decode a Message"))

if choice == "Encode a Message":
    st.header("Encode a Secret Message into an Image")
    uploaded_image = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=[
                                      "png", "jpg", "jpeg"], key="encode_uploader")
    secret_message = st.text_area(
        "Enter the Secret Message to Encode", key="encode_message")

    if uploaded_image:
        st.sidebar.image(
            uploaded_image, caption="Uploaded Image", use_column_width=True)

    if st.button("Encode", key="encode_button"):
        if uploaded_image and secret_message:
            encoded_image = encode(uploaded_image, secret_message)
            buffered = io.BytesIO()
            encoded_image.save(buffered, format="PNG")
            st.image(encoded_image, caption="Encoded Image",
                     use_column_width=True)
            st.success(
                "The secret message has been encoded into the image successfully!")
            st.download_button("Download Encoded Image", data=buffered.getvalue(
            ), file_name="encoded_image.png", mime="image/png")
        else:
            st.error("Please upload an image and enter a secret message.")

elif choice == "Decode a Message":
    st.header("Decode a Secret Message from an Image")
    uploaded_image = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=[
                                      "png", "jpg", "jpeg"], key="decode_uploader")

    if uploaded_image:
        st.sidebar.image(
            uploaded_image, caption="Uploaded Image", use_column_width=True)

    if st.button("Decode", key="decode_button"):
        if uploaded_image:
            decoded_message = decode(uploaded_image)
            st.success("The secret message has been decoded successfully!")
            st.text_area("Decoded Message", value=decoded_message, height=200)
        else:
            st.error("Please upload an image.")

st.sidebar.markdown("---")
st.sidebar.write(
    "This tool allows you to hide secret messages inside images and later retrieve them. Perfect for secure communication!")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "Made with ❤️ by [codewithyembot](https://codewithyembot.vercel.app/). created with [geeksforgeeks](https://www.geeksforgeeks.org/)")
st.sidebar.markdown("---")
