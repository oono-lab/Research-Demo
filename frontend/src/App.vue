<template>
  <div id="app" class="chat-container">
    <h1>研究デモ</h1>
    <div class="chat-box">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['chat-message', message.isUser ? 'user-message' : 'other-message']"
      >
        <span class="text">{{ message.text }}</span>
      </div>
    </div>
    <form @submit.prevent="sendMessage" class="chat-input">
      <input
        type="text"
        v-model="newMessage"
        :placeholder="placeholderText"
        class="message-input"
        required
      />
      <button type="submit" class="send-button">送信</button>
    </form>
    <div class="notice">
      ※これはChatGPTのAPIをまだ利用していないデモ版です。<br />
      ・赤玉4個と白玉2個が入っている袋Aと、赤玉3個と白玉2個が入っている袋Bがある。ぞれぞれの袋から1個ずつ玉を取り出すとき、2個とも赤玉が出る確率を求めよ。<br />
      ・数直線上で、点Pは原点Oを出発点とし、さいころを投げて2以下の目が出たときは正の向きに3だけ進み、他の目が出たときは負の向きに1だけ進むものとする。さいころを6回投げたとき、点Pが2の位置にいる確率を求めよ。<br />
      現在はこれらの問題文のみ対応しています。
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      messages: [],
      newMessage: "",
      stepIndex: 0,
      placeholderText: "メッセージを入力...",
      awaitingAnswer: false,
    };
  },
  methods: {
    async sendMessage() {
      if (this.newMessage.trim() !== "") {
        const userMessage = this.newMessage.trim();
        this.messages.push({ text: userMessage, isUser: true });
        this.newMessage = "";

        try {
          const response = await axios.post("http://127.0.0.1:5000/api/send", {
            message: userMessage,
            stepIndex: this.stepIndex,
            awaitingAnswer: this.awaitingAnswer,
            
          });

          const botResponse = response.data.response;
          const isCorrect = response.data.correct;
          const explanation = response.data.explanation;
          const Isfirst = response.data.isFirstMessage;

            if (this.awaitingAnswer) {
              if (isCorrect) {
              this.messages.push({ text: botResponse, isUser: false });
              this.messages.push({ text: explanation, isUser: false });
              this.stepIndex++;
              
              } else {
              this.messages.push({ text: botResponse, isUser: false });
              this.messages.push({ text: explanation, isUser: false });
            }
          } else {
            this.messages.push({ text: botResponse, isUser: false });
            if(Isfirst) this.awaitingAnswer = true;
            
          }
    
          
        } catch (error) {
          this.messages.push({ text: "エラーが発生しました。", isUser: false });
        }
      }
    },
  },
};
</script>



<style scoped>
.chat-container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
}

.chat-box {
  max-height: 400px;
  overflow-y: auto;
  padding: 10px;
  border: 1px solid #ddd;
  margin-bottom: 10px;
  background-color: #fff;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chat-message {
  max-width: 70%;
  padding: 10px;
  border-radius: 10px;
  font-size: 14px;
}

.user-message {
  align-self: flex-end;
  background-color: #daf7dc;
  color: #333;
}

.other-message {
  align-self: flex-start;
  background-color: #f0f0f0;
  color: #333;
}

.chat-input {
  display: flex;
  gap: 10px;
}

.message-input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.send-button {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  background-color: #3498db;
  color: #fff;
  cursor: pointer;
}

.send-button:hover {
  background-color: #2980b9;
}
/* 追加する注意書きのスタイル */
.notice {

  bottom: 10px;
  font-size: 12px;
  color: #555;
  background-color: #fff;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ddd;
  text-align: left;
  width: 90%;
  line-height: 1.5;
}
</style>