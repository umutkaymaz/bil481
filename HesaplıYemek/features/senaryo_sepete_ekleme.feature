Feature: Sepete Ürün ekleme
  
  Scenario: Sepete yemek ekleme
    Given Uygulama başlatılmıştır
    And Menüde "Pizza" adlı bir yemek listelenmektedir
    When Kullanıcı "Pizza" yemeğini seçer
    And Kullanıcı "+" butonuna tıklar
    Then Sepet etiketinde "Pizza: 1" görünmelidir