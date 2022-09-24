######################################################################
#参考にしたサイト様：                                                #
#--------------------------------------------------------------------#
#https://aidemy.net/magazine/1490/                                   #
#ヘッダーとフッターのひな型、画像分類のソースを拝借しました。        #
#--------------------------------------------------------------------#
#https://www.webcreatorbox.com/tech/javascript-particles             #
#背景エフェクトを拝借しました。                                      #
#--------------------------------------------------------------------#
#その他エンジニア質問サイトでメニューに戻るテキスト切り替えアイデア、#
#ドロップダウンメニューの値保持について質問しています。              #
#くそコードで申し訳ないです。                                        #
######################################################################

from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model

import trans_text_ja_2
import speech_synthesis
import image_
import comp_sentiment

app = Flask(__name__)

# 直接アクセスした場合もメニューに強制遷移
@app.route('/')
def index():
    return render_template('menu.html')

# メニュー
@app.route('/menu/')
def trans_menu():
    return render_template('menu.html')

# パラメータがある場合は、翻訳して表示する
@app.route('/trans/', methods=['GET', 'POST'])
def trans():
    #翻訳
    lang = [
    {"display": "ドイツ語", "code": "de"},
    {"display": "英語", "code": "en"},
    {"display": "スペイン語", "code": "es"},
    {"display": "フランス語", "code": "fr"},
    {"display": "イタリア語", "code": "it"},
    {"display": "ポルトガル語", "code": "pt"},
    {"display": "日本語", "code": "ja"},
    {"display": "韓国語", "code": "ko"},
    {"display": "ヒンディー語", "code": "hi"}
    ]
    # 読み上げ
    polly_lang = {"de": "Hans", "en": "Emma", "es": "Lucia", "fr": "Celine",
              "it": "Giorgio", "pt": "Cristiano", "ja": "Mizuki", "ko": "Seoyeon", "hi": "Aditi"}
    try:
        if request.method == 'POST':
            # リクエストパラメータを読み込む
            in_text = request.form['input_text']
            language = request.form['lang']

            #取得したインデックスに対応する辞書の中のcodeで言語コードを取得
            targetlanguagecode = lang[int(language)]['code']

            #選択された言語のselectedをTrueに
            lang[int(language)]['selected'] = True

            #文字数カウント再出力用
            in_text_length = in_text.replace( '\n' , '' )

            # 値を取得
            value = request.form.get('send', None)

            # 取得した値が翻訳なら
            if value == "翻訳する":
                # それぞれ引数を持って翻訳
                result = trans_text_ja_2.translate(in_text, targetlanguagecode)

                # 翻訳済みテキストをグローバル変数で取得
                global transretedtext
                transretedtext = result['TranslatedText']

                # 翻訳の結果を返す
                return render_template('translate.html',
                                        input_text=in_text,
                                        output_text=transretedtext,
                                        lang=lang,
                                        input_lengh=f"{len(in_text_length)}/5000")

            elif value == "音声合成":

                #viceIDを取得
                trget_langcode = polly_lang[targetlanguagecode]

                # 引数をもって音声ファイル作成
                path = speech_synthesis.polly(transretedtext, trget_langcode)

                # 音声合成の結果を返す
                return render_template('translate.html',
                                        input_text=in_text,
                                        output_text=transretedtext,
                                        lang=lang, polly=f"../{path}",
                                        input_lengh=f"{len(in_text_length)}/5000")

            elif value == "感情分析":

                # 分析結果を取得
                sentiment = comp_sentiment.sentimentsearch(transretedtext, targetlanguagecode)

                # 感情分析の結果を返す
                return render_template('translate.html',
                                        input_text=in_text,
                                        output_text=transretedtext,
                                        lang=lang,
                                        polly='',
                                        sentiment=f"分析結果：{sentiment['Sentiment']}",
                                        input_lengh=f"{len(in_text_length)}/5000")

            elif value == "ファイルを読み込む":

                #保存したファイルを読み込んで表示
                f = request.files.get('file')
                filename = secure_filename(f.filename)
                filepath = f'static/text/{filename}'
                f.save(filepath)
                data = ""
                with open(filepath, 'r', encoding='UTF-8') as f:
                    data = f.read()

                #結果を返す
                return render_template('translate.html',
                                        input_text=data,
                                        output_text='',
                                        lang=lang,
                                        input_lengh=f"{len(data)}/5000")

        # 翻訳画面をまっさらで表示
        return render_template('translate.html',
                                input_text='',
                                output_text='',
                                lang=lang,
                                input_lengh="0/5000")

    #すべての例外をキャッチし、エラー画面に飛ばす
    except Exception:
        return render_template('error.html')




# 画像分析
@app.route('/image_menu/', methods=['GET'])
def test():
    return render_template("image_menu.html")

#小峠英二判定の時
@app.route('/kotougeeiji/', methods=['GET', 'POST'])
def image_kotouge():
    try:
        classes = ['小峠英二', '小峠英二ではない']
        # 学習済みモデルをロード
        model = load_model('static/model/kotouge.h5')
        if request.method == 'POST':

            # 読み込んで保存
            f = request.files.get('file')
            filename = secure_filename(f.filename)
            filepath = f'static/image/{filename}'
            f.save(filepath)

            #画像分類を実行
            pred_answer = image_.image_start(filepath, model, classes)
            action = "/kotougeeiji/"

            #結果を表示
            return render_template("image.html",
                                    action=action,
                                    answer=pred_answer,
                                    filepath=f"../{filepath}")

        #初期は答えを空にして表示
        return render_template("image.html", answer="")

    #すべての例外をキャッチし、エラー画面に飛ばす
    except Exception:
        return render_template('error.html')

#犬猫判定の時
@app.route('/dog_cat/', methods=['GET', 'POST'])
def image_inuneko():
    try:
        classes = ['犬', '猫']
        # 学習済みモデルをロード
        model = load_model('static/model/dog_cat.h5')
        if request.method == 'POST':

            # 読み込んで保存
            f = request.files.get('file')
            filename = secure_filename(f.filename)
            filepath = f'static/image/{filename}'
            f.save(filepath)

            #画像分類を実行
            pred_answer = image_.image_start(filepath, model, classes)
            action = "/dog_cat/"

            #結果を表示
            return render_template("image.html",
                                    action=action,
                                    answer=pred_answer,
                                    filepath=f"../{filepath}")

        #初期は答えを空にして表示
        return render_template("image.html", answer="")

    #すべての例外をキャッチし、エラー画面に飛ばす
    except Exception:
        return render_template('error.html')

#おまじない
if __name__ == '__main__':
    app.run(debug=True)
