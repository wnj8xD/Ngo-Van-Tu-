import streamlit as st
import requests
import io
import base64
from modules import feedback

def show_home(username):

    from PIL import Image

    # Cấu hình giao diện Streamlit
    st.markdown("📱 You can take **one** photo or upload **one** image of the leaf on the plant you want to test by clicking the **Browse files** button, then selecting the image you want to upload")
    st.markdown("Then the plant species name and predicted diseases along with their correct probability will be **displayed on the screen**, pay attention!!")

    # Upload ảnh
    uploaded_file = st.file_uploader("📤 Upload image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="🖼️ **Uploaded successfully**", use_container_width=True)

        if st.button("🔍 Identify plant type and diseases"):
            # Chuyển ảnh sang dạng base64
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            # ---------- STEP 1: Phân loại loại cây ----------
            st.subheader("🧬 Identify the type of leaf...")
            leaf_type_url = "https://serverless.roboflow.com/infer/workflows/i30/leaf-type"  # 👉 THAY bằng workflow đúng
            leaf_type_key = "Sq8AwQQ64AZEGfvmjn03"  # 👉 THAY bằng API KEY đúng

            leaf_payload = {
                "api_key": leaf_type_key,
                "inputs": {
                    "image": {
                        "type": "base64",
                        "value": img_str
                    }
                }
            }

            leaf_response = requests.post(leaf_type_url, json=leaf_payload)
            leaf_result = leaf_response.json()
            print(leaf_result)
            try:
                prediction_data = leaf_result['outputs'][0]['predictions']
                prediction_list = prediction_data.get('predictions', [])

                if not prediction_list:
                    st.error("❌ Plant species not identified. Please try again with a better quality image.")
                    st.stop()

                # Lấy class có độ tin cậy cao nhất
                top_class = sorted(prediction_list, key=lambda x: x['confidence'], reverse=True)[0]['class']
                leaf_type = top_class.split("_")[0]  # ví dụ: 'coffee_leaf_healthy' -> 'coffee'

                st.success(f"📗🍃 Plant leaf type: **{leaf_type.upper()}**")

            except:
                st.error("❌ Plant species not identified. Please try again with a better quality image.")
                st.stop()

            # ---------- STEP 2: Dự đoán bệnh theo loại cây ----------
            st.subheader("🦠 Detecting disease...")

            api_config = {
            "durian": {
                "url": "https://serverless.roboflow.com/infer/workflows/i30/durian-deseases-detection",
                "key": "Sq8AwQQ64AZEGfvmjn03"
            },
            "lemon": {
                "url": "https://serverless.roboflow.com/infer/workflows/i30/lemon-deseases-detection",
                "key": "Sq8AwQQ64AZEGfvmjn03"
            },
            "coffee": {
                "url": "https://serverless.roboflow.com/infer/workflows/i30/coffee-deseases-detection",
                "key": "Sq8AwQQ64AZEGfvmjn03"
            }
            }
            

            if leaf_type not in api_config:
                st.error(f"❌ No disease support for this plant type: {leaf_type}")
                st.stop()

            disease_payload = {
                "api_key": api_config[leaf_type]['key'],
                "inputs": {
                    "image": {
                        "type": "base64",
                        "value": img_str
                    }
                }
            }

            disease_response = requests.post(api_config[leaf_type]['url'], json=disease_payload)
            disease_response = disease_response.json()
            print(disease_response)
            try:
                preds = disease_response['outputs'][0]['predictions']['predictions']
                if preds:
                    st.subheader("📌 Diseases detected on leaves:")
                    for pred in preds:
                        disease_class = pred['class']
                        confidence = pred['confidence']
                        st.markdown(f"✅ **{disease_class}** ({confidence*100:.2f}%)")
                        

                else:
                    st.error("❌ No disease was detected on this leaf.")
               

            except Exception as e:
                st.error("⚠️ Error processing disease recognition results.")
                st.exception(e)

