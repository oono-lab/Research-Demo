from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# new_questionsリスト
new_questions = [
    "赤玉4個と白玉2個が入っている袋Aと、赤玉3個と白玉2個が入っている袋Bがある。ぞれぞれの袋から1個ずつ玉を取り出すとき、2個とも赤玉が出る確率を求めよ。",
    "数直線上で、点Pは原点Oを出発点とし、さいころを投げて2以下の目が出たときは正の向きに3だけ進み、他の目が出たときは負の向きに1だけ進むものとする。さいころを6回投げたとき、点Pが2の位置にいる確率を求めよ。"
]

# GPT_OUTPUT_Senteceリスト
GPT_OUTPUT_Sentece = [
    """
    ステップ1 : 袋Aに含まれる玉の総数を求めよ。、6、袋Aには赤玉が4個、白玉が2個含まれているので、合計を計算してください。
    ステップ2 : 袋Bに含まれる玉の総数を求めよ。、5、袋Bには赤玉が3個、白玉が2個含まれているので、合計を計算してください。
    ステップ3 : 袋Aで赤玉を引く確率を求めよ。、2/3、赤玉の数を袋A全体の玉の数で割ってください。
    ステップ4 : 袋Bで赤玉を引く確率を求めよ。、3/5、赤玉の数を袋B全体の玉の数で割ってください。
    ステップ5 : 両方で赤玉が出る確率を求めよ。、2/5、袋Aと袋Bで赤玉を引く確率を掛け合わせてください。
    """,
    """
    ステップ1 :さいころを1回投げたとき、2以下の目が出る確率を求めよ。、1/3、さいころの出目のうち1と2が該当し、その数を全ての出目の数で割る。
    ステップ2 :さいころを1回投げたとき、3以上の目が出る確率を求めよ。、2/3、さいころの出目のうち3, 4, 5, 6が該当し、その数を全ての出目の数で割る。
    ステップ3 :点Pが位置2に到達するために、正の向きに進む回数を求めよ。、2、位置2にいる条件式 3k−(6−k)=2 を解く。
    ステップ4 :点Pが位置2に到達するための負の向きに進む回数を求めよ。、4、6回の投げのうち、正の向きに進む回数を引く。
    ステップ5 : さいころを6回投げたとき、正の向きに進む回数が2回になる確率を求めよ。、80/243、二項分布の公式を使う。
    """
]

def remove_newlines_and_spaces(text):
    return ' '.join(text.split())

def extract_steps_and_answers(gpt_output_sentence):
    import re
    steps_dict = {}
    pattern = r"ステップ\d+\s*:\s*(.+?)、\s*([\d/\.]+)\s*、\s*(.+?)(?=\s*ステップ\d+|$)"
    matches = re.findall(pattern, gpt_output_sentence, re.DOTALL)
    for step_and_question, answer, explanation in matches:
        steps_dict[step_and_question.strip()] = {
            "answer": answer.strip(),
            "explanation": explanation.strip()
        }
    return steps_dict

def extract_to_lists(steps_dict):
    step_and_question_list = []
    correct_answer_list = []
    explanation_list = []
    for step_and_question, step_data in steps_dict.items():
        step_and_question_list.append(step_and_question)
        correct_answer_list.append(step_data["answer"])
        explanation_list.append(step_data["explanation"])
    return step_and_question_list, correct_answer_list, explanation_list

@app.route("/api/send", methods=["POST"])
def handle_message():
    data = request.json
    user_message = data.get("message", "")
    step_index = data.get("stepIndex", 0)
    awaitingAnswer = data.get("awaitingAnswer", False)

    if (user_message in new_questions) and awaitingAnswer==False:
        index = new_questions.index(user_message)
        cleaned_text = remove_newlines_and_spaces(GPT_OUTPUT_Sentece[index])
        steps_dict = extract_steps_and_answers(cleaned_text)
        step_and_question_list, correct_answer_list, explanation_list = extract_to_lists(steps_dict)
        return jsonify({
            "response": step_and_question_list[0],
            "correct": None,
            "explanation": None,
            "isFirstMessage": True
        })
    if awaitingAnswer:
        for i, question in enumerate(new_questions):
            cleaned_text = remove_newlines_and_spaces(GPT_OUTPUT_Sentece[i])
            steps_dict = extract_steps_and_answers(cleaned_text)
            step_and_question_list, correct_answer_list, explanation_list = extract_to_lists(steps_dict)

            if step_index < len(correct_answer_list):
                if user_message == correct_answer_list[step_index]:
                    if step_index != len(correct_answer_list)-1:
                        return jsonify({
                            "response": "正解です！",
                            "correct": True,
                            "explanation": step_and_question_list[step_index+1],
                            "isFirstMessage": True
                        })
                    else:
                        return jsonify({
                            "response": "これで全問正解です！",
                            "correct": True,
                            "explanation":" お疲れさまでした！",
                            "isFirstMessage": True
                        })
                else:
                    return jsonify({
                        "response": "不正解です。",
                        "correct": False,
                        "explanation": explanation_list[step_index],
                        "isFirstMessage": True
                    })
    return jsonify({"response": "他の問題でお願いします。", "correct": None, "explanation": None,"isFirstMessage": False})

if __name__ == "__main__":
    app.run(debug=True)
