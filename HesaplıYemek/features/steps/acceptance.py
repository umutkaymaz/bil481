from behave import given, when, then
import config
import GUI_actions

@given("Uygulama başlatılmıştır")
def step_impl(context):
    context = config.master
    GUI_actions.fiyatlari_getir(config.menu_data,config.favorite_var)
    print("Uygulama başlatıldı.")

@given('Menüde "{yemek}" adlı bir yemek listelenmektedir')
def step_impl(context, yemek):
    print(f"Menüde {yemek} listelendi.")

@when('Kullanıcı "{yemek}" yemeğini seçer')
def step_impl(context, yemek):
    config.selected_food_var
    GUI_actions.yemek_sec(event, config.sepet, config.selected_food_var, config.miktar_var)
    print(f"Kullanıcı {yemek} yemeğini seçti.")

@when("Kullanıcı \"+\" butonuna tıklar")
def step_impl(context):
    # "+" butonuna tıklama işlemini simüle eden kodu çalıştırın.
    # Örneğin, yemek_ekle fonksiyonunu çağırabilirsiniz.
    # Yemek ekleme fonksiyonunuz gereken parametreleri almalı.
    print("Kullanıcı '+' butonuna tıkladı.")
    # Yemek ekleme işlemini gerçekleştirin.
    # Örnek:
    # yemek_ekle(joker_yemeksepeti, joker_getir, joker_migros, config.sepet_icerik, config.selected_food_var, config.sepet, config.miktar_var, config.menu_data)

@then('Sepet etiketinde "{expected_text}" görünmelidir')
def step_impl(context, expected_text):
    # Sepet etiketinin beklenen değeri içerdiğini doğrulayın.
    actual_text = config.sepet_icerik.get()  # Bu, GUI label'ındaki metin olabilir.
    assert expected_text in actual_text, f"Beklenen: {expected_text}, Alınan: {actual_text}"
    print("Sepet etiketi doğrulandı.")