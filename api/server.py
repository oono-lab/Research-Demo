from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def extract_steps_and_answers(gpt_output_sentence):
    steps_dict = {}
    pattern = r"ステップ\d+\s*:\s*(.+?)、\s*([\d/\.]+)\s*、\s*(.+?)(?=\s*ステップ\d+|$)"
    matches = re.findall(pattern, gpt_output_sentence, re.DOTALL)

    for step_and_question, answer, explanation in matches:
        step_data = {
            "answer": answer.strip(),
            "explanation": explanation.strip()
        }
        steps_dict[step_and_question.strip()] = step_data

    return steps_dict
def remove_newlines_and_spaces(text):
    # 改行と余分な空白を1つのスペースに置き換える
    cleaned_text = ' '.join(text.split())
    return cleaned_text
def extract_to_lists(steps_dict):
    step_and_question_list = []
    correct_answer_list = []
    explanation_list = []

    for step_and_question, step_data in steps_dict.items():
        step_and_question_list.append(step_and_question)
        correct_answer_list.append(step_data["answer"])
        explanation_list.append(step_data["explanation"])

    return step_and_question_list, correct_answer_list, explanation_list

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    input_sentence = data.get("input_sentence", "")

    # シナリオに応じた出力
    GPT_OUTPUT_Sentece = [
        """
        ステップ1 : 袋Aに含まれる玉の総数を求めよ。、6、袋Aには赤玉が4個、白玉が2個含まれているので、合計を計算してください。

        ステップ2 : 袋Bに含まれる玉の総数を求めよ。、5、袋Bには赤玉が3個、白玉が2個含まれているので、合計を計算してください。

        ステップ3 : 袋Aで赤玉を引く確率を求めよ。、2/3、赤玉の数を袋A全体の玉の数で割ってください。

        ステップ4 : 袋Bで赤玉を引く確率を求めよ。、3/5、赤玉の数を袋B全体の玉の数で割ってください。

        ステップ5 : 両方で赤玉が出る確率を求めよ。、2/5、袋Aと袋Bで赤玉を引く確率を掛け合わせてください。
        """,
        """
        ステップ1 :さいころを1回投げたとき、2以下の目が出る確率を求めよ。
        、
        1/3、
        さいころの出目のうち1と2が該当し、その数を全ての出目の数で割る。


        ステップ2 :さいころを1回投げたとき、3以上の目が出る確率を求めよ。
        、
        2/3、
        さいころの出目のうち3, 4, 5, 6が該当し、その数を全ての出目の数で割る。


        ステップ3 :点Pが位置2に到達するために、正の向きに進む回数を求めよ。、
        2、位置2にいる条件式 3k−(6−k)=2 を解く。


        ステップ4 :点Pが位置2に到達するための負の向きに進む回数を求めよ。
        、
        4
        、
        6回の投げのうち、正の向きに進む回数を引く。


        ステップ5 : さいころを6回投げたとき、正の向きに進む回数が2回になる確率を求めよ。
        、
        80/243、
        二項分布の公式を使う。
        """
    ]

    new_questions = [
        "赤玉4個と白玉2個が入っている袋Aと、赤玉3個と白玉2個が入っている袋Bがある。ぞれぞれの袋から1個ずつ玉を取り出すとき、2個とも赤玉が出る確率を求めよ。",
        "数直線上で、点Pは原点Oを出発点とし、さいころを投げて2以下の目が出たときは正の向きに3だけ進み、他の目が出たときは負の向きに1だけ進むものとする。さいころを6回投げたとき、点Pが2の位置にいる確率を求めよ。"
    ]

    matching_index = next((i for i, q in enumerate(new_questions) if q.strip() == input_sentence.strip()), -1)
    if matching_index == -1:
        return jsonify({"error": "一致する質問が見つかりませんでした。"})

    selected_output = GPT_OUTPUT_Sentece[matching_index]
    steps_dict = extract_steps_and_answers(selected_output)
    step_and_question_list, correct_answer_list, explanation_list = extract_to_lists(steps_dict)

    return jsonify({
        "step_and_question_list": step_and_question_list,
        "correct_answer_list": correct_answer_list,
        "explanation_list": explanation_list
    })

if __name__ == "__main__":
    app.run(debug=True)
