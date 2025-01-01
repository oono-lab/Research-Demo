from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# new_questionsリスト
new_questions = [
    "赤玉4個と白玉2個が入っている袋Aと、赤玉3個と白玉2個が入っている袋Bがある。ぞれぞれの袋から1個ずつ玉を取り出すとき、2個とも赤玉が出る確率を求めよ。",
    "数直線上で、点Pは原点Oを出発点とし、さいころを投げて2以下の目が出たときは正の向きに3だけ進み、他の目が出たときは負の向きに1だけ進むものとする。さいころを6回投げたとき、点Pが2の位置にいる確率を求めよ。",
    "2個のサイコロを同時に投げるとき、出る目の和が４になる確率を求めよ。",
    "１から１００までの番号をつけた１００枚のカードから１枚を取り出すとき、その番号が４の倍数または６の倍数である確率を求めよ。",
    "１５本のくじの中に当たりくじが５本ある。この中から２本のくじを同時に引くとき、少なくとも１本が当たる確率を求めよ。",
    "１個のさいころと１枚の硬貨を投げるとき、さいころは６の約数の目が出て、硬貨は表が出る確率を求めよ。"
    
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
    """,
    """
    ステップ1: 2個のサイコロを投げたときに考えられるすべての目の組み合わせの数は？、36、各サイコロは6面あり、それぞれ独立して出る目が決まります。
    ステップ2: サイコロの目の和が4になる場合のすべての組み合わせの数は？、3、和が4になる組み合わせを列挙して数えます。
    ステップ3: 確率を求めるために、和が4になる組み合わせ数を全体の組み合わせ数で割った結果は？、1/12、確率は成功する場合の数を全体の数で割って求めます。
    """,
    """
    ステップ1: 1から100までの整数のうち、4の倍数は何個ありますか？、25、100を4で割ってその整数部分を取ります。
    ステップ2: 1から100までの整数のうち、6の倍数は何個ありますか？、16、100を6で割ってその整数部分を取ります。
    ステップ3: 1から100までの整数のうち、12の倍数は何個ありますか？、8、100を12で割ってその整数部分を取ります。
    ステップ4: 4または6の倍数の数を求めなさい。、33、「4の倍数 + 6の倍数 - 12の倍数」で計算します。
    ステップ5: 全体のカード枚数に対して、4または6の倍数である確率を分数で表してください。、33/100、4または6の倍数の数を全体のカード数（100）で割ります。
    """,
    """
   ステップ1:「15本のくじから2本を選ぶ場合の全組み合わせ数はいくつですか？」、105、組み合わせの公式15C2を計算する。
   ステップ2:「外れくじが10本のとき、10本から2本を選ぶ組み合わせ数はいくつですか？」、45、同じく組み合わせの公式を使用します。
   ステップ3:「2本とも外れくじを引く確率はいくつですか？」、3/7、全体の組み合わせ数分の外れくじの組み合わせ数で確率を求めます。
   ステップ4:「少なくとも1本が当たる確率はいくつですか？」、4/7、全確率1から「2本とも外れる確率」を引きます。
   """,
   """
   ステップ1:サイコロを投げたとき、6の約数の目が出る数はいくつか？、4、6の約数をリストアップするだけです。
   ステップ2:サイコロの目が6の約数となる確率はいくつか？、2/3、全体の目の数と6の約数の目の数の比率を計算します。
   ステップ3:硬貨を投げたとき、表が出る確率はいくつか？、1/2、硬貨は表と裏の2つの可能性しかありません。
   ステップ4:サイコロが6の約数の目を出し、硬貨が表を出す確率はいくつか？、1/3、2つの独立した確率を掛け合わせます。
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
