import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import google.generativeai as genai
import os

def main():

  st.markdown("""
    <style>
      .title_format {
        font-style: bold;
        font-size:40px !important;
        background-color: pink;
        width: 580px;
        height: 50px;     
      }
    </style>
  """, unsafe_allow_html=True)
  st.markdown('<p class="title_format">詐欺にだまされないお守りに!</p>', unsafe_allow_html=True)

  st.markdown("""
    <style>
      .subtitle_format {
              
        font-style: bold;  
        font-size:25px !important;
        background-color: pink;
        width: 500px;
        height: 50px;
      }
    </style>
  """, unsafe_allow_html=True)
  st.markdown('<p class="subtitle_format">人工知能(AI)の「お守りAI(アイ)ちゃん」が</p>', unsafe_allow_html=True)
  st.markdown('<p class="subtitle_format">あなたの相談相手になります</p>', unsafe_allow_html=True)

  # API_KEYの設定方式に注意
  # Google AI Studioの"Get code"にあるcodeの設定ではKeyErrorが出た
  # API_KEYを環境変数に設定
  APIKEY=os.getenv('Gemini_API_KEY')
  genai.configure(api_key=APIKEY)

  # Create the model
  # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel

  safety_setting=[
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_ONLY_HIGH"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_ONLY_HIGH"
    },
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_ONLY_HIGH"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_ONLY_HIGH"
    }
  ]

  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 5000,
    "response_mime_type": "text/plain",  
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings = safety_setting,
    # See https://ai.google.dev/gemini-api/docs/safety-settings
  )

  chat_session = model.start_chat(
    history=[
    ]
  )

  st.markdown("""
    <style>
      .text_area_format {
        font-size:20px !important;
        # background-color: green;
      }
    </style>
  """, unsafe_allow_html=True)
  st.markdown('<p class="text_area_format">あなたがお守りアイちゃんにききたいことを書いて下さい:</p>', unsafe_allow_html=True)
  # 入力文字数を30字に制限
  question=st.text_area("", max_chars=30, height=30)
  

  prompt_0="あなたは詐欺の防止法についての専門家です。どんな質問にも対応できます。"

  # ここを色々変えることでGeminiのresponseに影響する
  prompt_1="以下の質問に回答願います。丁寧な言葉で具体的に回答してください。"

  # 詐欺耐力を向上するようなプロンプト
  prompt_2="自分の身は自分で守れるように、自分自身でも色々考えるように促してください。"
  
  prompt_3="質問でない場合には、質問をするように促してください。"
  
  prompt_4="詐欺の相談以外の質問を厳密に判断して回答を拒否してください。"

  prompt_5="法律や倫理に反する質問は回答を拒否してください。"
  
  prompt=prompt_0+prompt_1+prompt_2+prompt_3+prompt_4+prompt_5+question

  st.write("")

  # \nの前に半角スペースを2個入れる
  action=st.button("ここを押すとお守りアイちゃんの回答が表示されます。  \nお守りアイちゃんは一生懸命考えているので少し時間がかかります。")
  if action:
    response = chat_session.send_message(prompt)
    st.write("")
    st.write("")

    st.markdown("""
    <style>
      .write_format {
        font-size:20px !important;
        # background-color: blue;
      }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="write_format">お守りアイちゃんからのアドバイスです:</p>', unsafe_allow_html=True)
    # with st.container():

    md=response.text

    st.markdown(md)
      # st.text_area("生成AIのアドバイスです。", value=st.markdown(response.text), height=500)

if __name__=="__main__":
  main()
