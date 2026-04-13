
md5_path = "D:/zhuomian/rag项目/pythonProject2/rag项目/md5_text"
collection_name="rag"  #数据库
embedding_model_name="text-embedding-v4"
persist_directory="D:/zhuomian/rag项目/pythonProject2/rag项目/chroma_base"
chunk_size =100
chunk_overlap=20
separators=[",", ".", "/n", "?", " ", "，", "。", "\n","\n\n", "？", "！", "!", ]
max_len=300
similarity =3

chat_model_name ="qwen3-max"

session_config = {
        "configurable": {"session_id": "user_002"}
    }