from langchain_community.chat_models import BedrockChat
from langchain_core.messages import HumanMessage
import json

# 使用するLLMモデルを宣言
chat = BedrockChat(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    model_kwargs={
        "max_tokens": 1000,
        "temperature": 0.5,
    },
)

# Lambdaハンドラー
def lambda_handler(event, context):
    # for debug
    print(f"Received event: {json.dumps(event, ensure_ascii=False)}")
    # イベントJSONから入力パラメーターを取得
    input_text = event.get("input_text")
    # メインの処理を呼び出す
    output_text = chat_conversation(input_text)
    # Lambda関数のレスポンスを返す
    return {
        "output_text": output_text,
    }

# メイン処理
def chat_conversation(input_text: str) -> str:
    # LLMに与えるプロンプトを設定
    messages = [
        HumanMessage(
            content=input_text
        ),
    ]

    # LLMにプロンプトを与えて、応答を含む結果を得る
    result = chat.invoke(messages)
    # デバック用
    print(f"Result: {result}")

    # LLMが返した最新の応答テキストを抽出
    output_text = result.content

    return output_text
