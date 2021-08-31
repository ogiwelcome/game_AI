from tensorflow.keras.layers import Activation, Add, BatchNormalization, Conv2D, Dense, GlobalAveragePooling2D, Input
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2
from tensorflow.keras import backend as K
import os
DN_FILTERS = 128
DN_RESIDUAL_NUM = 16
DN_INPUT_SHAPE = (8,8,2)
DN_OUTPUT_SIZE=65
def conv(fliters):
    return Conv2D(filters, 3, padding='same', use_bias=False, kernel_initializer='he_normal', kernel_regularizer=l2(0.0005))
def residual_block():
    def f(x):
        sc = x
        x = conv(DN_FILTERS)(x)
        x = BatchNormalization()(x)
        x = Activation()(x)
        x = conv(DN_FILTERS)(x)
        x = BatchNormalization()(x)
        x = Add()([x,sc])
        x = Activation('relu')(x)
        return x
    return f
def dual_network():
    if os.path.exists('./model/best.h5'):
        return
    # 入力層
    input = Input(shape=DN_INPUT_SHAPE)
    # 畳み込み層
    x = conv(DN_FILTERS)(input)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    # 残差ブロック
    for rep in range(DN_RESIDUAL_NUM):
        x = residual_block()(x)
    # プーリング層
    x = GlobalAveragePooling2D()(x)
    # ポリシー出力
    p = Dense(DN_OUTPUT_SIZE, kernel_regularizer=l2(0.0005), activation='softmax', name='pi')(x)
    # バリュー出力
    v = Dense(1,kernel_regularizer=l2(0.0005))(x)
    v = Activation('tanh', name='v')(v)
    #　モデル作成
    model = Model(inputs=input, outputs=[p,v])
    # 保存
    os.makedirs('./model/',exist_ok=True)
    model.save('./model/best.h5')
    # 破棄
    K.clear_session()
    del model
if __name__=='__main__':
    dual_network()