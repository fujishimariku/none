from tensorflow.keras.preprocessing import image
import numpy as np

#画像分類
def image_start(filepath, model, classes):
    #画像サイズ
    img_size = 64

    # 受け取った画像を読み込み、np形式に変換
    img = image.load_img(filepath, grayscale=True,
                         target_size=(img_size, img_size))
    img = img.convert('RGB')

    # 画像データを64 x 64に変換
    img = img.resize((img_size, img_size))

    # 画像データをnumpy配列に変換、予測し結果を返す
    img = np.asarray(img)
    img = img / 255.0
    result = model.predict(np.array([img]))
    predicted = result.argmax()
    return f"分析結果は {classes[predicted]} です。"
