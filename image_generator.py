import openai
from PIL import Image
import requests
from io import BytesIO
import streamlit as st
import time

def prompt_builder(input_text,design_choice,sub_design_choice,color_choice,camera_angles,illumination_type):
    if len(input_text) > 2:
        if design_choice != "None":
            prompt = f"Design a high resolution {sub_design_choice} {design_choice} of {input_text}."
            if len(color_choice)>1:
                background_colour_str = ", ".join(color_choice)
                prompt = prompt + f" Use shades of {background_colour_str} colours in the background."
            else:
                prompt = prompt + f"Use a {color_choice[0]} background to capture the object of the image"
            prompt = prompt + f"Use {camera_angles} and enhance the image with {illumination_type}"
        else:
            prompt = f"Design a high resolution image for {input_text}"
    else:
        st.write("Include objects, colours, locations, surroundings, people to generate relevant images")
    return prompt


st.title("ImaGen - Image Generator")

with st.sidebar:
    st.title("ImaGen")
    st.subheader("Image Generator")
    openai_key = st.text_input("API-Key: ",placeholder = "Enter your API key here")
    st.write("---------------------------------------------")
    st.write("Include objects, colours, locations, surroundings, people...")
    input_text = st.text_input("Add text input here:",placeholder = "An astronaut reading a book in space")
    st.write("---------------------------------------------")
    st.write("Select the styles ")
    design_choice = st.selectbox("Image category",("photography","digital art","fine art","none"))
    if design_choice == "photography":
        sub_design_choice = st.selectbox("Image style", ("realistic","vibrant","minimalist", "neon", "filimic"))
    elif design_choice == "digital art":
        sub_design_choice = st.selectbox("Image style", ("3D","colourful","retrowave", "psychedelic", "3D model","concept art","gradient","anime","retro anime","dreamlike"))
    elif design_choice == "fine art":
        sub_design_choice = st.selectbox("Image style", ("watercolor","colour pencil","stained glass", "ink print", "oil painting","abstract"))
    elif design_choice == "none":
        sub_design_choice = "none"
    st.write("---------------------------------------------")
    st.write("Advanced features")
    color_choice = st.multiselect("Background colour", ("red", "blue", "green", "yellow", "orange", "purple", "pink", "black", "white", "gray", "brown", "cyan", "magenta", "teal", "lime", "maroon", "navy", "olive", "silver", "violet", "beige", "gold", "khaki", "lavender", "orchid", "plum", "salmon", "tan", "turquoise", "white"),("black"),max_selections=3)
    camera_angles = st.selectbox("Camera angles",("random shots","close-up shot", "high-angle shot", "mid-angle shot","low-angle shot","elevated-angle shot", "top-down shot","macro shots","bird's-eye view"))
    illumination_type = st.selectbox("Lighting",("random lighting","soft golden lighting", "soft diffused lighting", "dynamic directional lighting","natural lighting","dramatic side lighting", "warm sun lighting","dim lighting","warm mood lighting","bright lighting","cool toned lighting","warm toned lighting"))
    st.write("---------------------------------------------")
    num = st.slider("Select the number of background designs to generate", 1, 10, 3)
    size_choice = st.radio("Select the size of the background design", ( "1024x1024","512x512","256x256"))
    st.write("You selected:", size_choice)
    st.write("---------------------------------------------")
    clicked = st.button("Generate Image")
    

if clicked:
    if len(openai_key) > 1:
        openai.api_key = openai_key
        st.write("Generating Images...")
        time.sleep(2)
        my_bar = st.progress(0)
        prompt = prompt_builder(input_text,design_choice,sub_design_choice,color_choice,camera_angles,illumination_type)
        response = openai.Image.create(
        prompt=prompt,
        n=num,
        size=size_choice
        )
        #image_url = response['data'][0]['url']
        data = response['data']
        try:
            with st.container():
                for ind,res in enumerate(data):
                    url = res['url']
                    response = requests.get(url)
                    img = Image.open(BytesIO(response.content))
                    #img.save('/Users/aadithyuenair/Documents/Projects/yarnit/knowledge-graph-api/images/{}-{}.png'.format(prompt,ind))
                    st.image(img, caption='{}-{}'.format(prompt,ind), use_column_width=True)
                    btn = st.download_button(
                                                label="Download image",
                                                data=BytesIO(response.content),
                                                file_name='{}-{}.png'.format(prompt,ind), 
                                                mime="image/png"
                                            )
                    #st.download_button(label="Download", data=img, file_name='{}-{}.png'.format(prompt,ind), mime='application/octet-stream')
                    my_bar.progress((ind+1)/num)
        except Exception as e:
            st.write(e.args[0])
            st.error('Please enter a valid API key!', icon="🚨") 
    else:
        st.error('Please enter an API key!', icon="🚨")
