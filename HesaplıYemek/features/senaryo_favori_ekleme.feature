Feature: Favori Restoran ekleme
  
  Scenario: Favori Listesine restoran ekleme
    Given Uygulama başladı
    And Kullanıcı "Söğütözü, Söğütözü Cd. No:43, 06510 Çankaya/Ankara" seklinde konumunu girmistir
    And Kullanıcı "Öncü Döner" isminde restoran bilgisini girer
    When Kullanıcı favori butonuna tıklar
    Then Favori listesinde  "Söğütözü, Söğütözü Cd. No:43, 06510 Çankaya/Ankara - Öncü Döner" görünmelidir