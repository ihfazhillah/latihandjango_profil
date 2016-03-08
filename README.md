# latihandjango_profil
Latihan Django, Profil App

Profil app, adalah projek sederhana untuk "melancarkan" serta "mempelajari" beberapa fitur dalam django. Diantara hal yang kita (saya) pelajari dengan bolak balik buka manual :
- Formset, form
- membuat login, logout view
- membuat custom validator
Dan yang lainnya. Saya menggunakan metode TDD (Test Driven Development) didalam projek ini.

### Profil App feature:
- Login logout
- membuat profil baru berikut phone/web url
- mengedit profil yang ada berikut phone/web url

### Instalasi
Hanya clone repository ini, dan letakkan dimana anda suka, dan kemudian lakukan 
`./manage.py makemigrations`
`./manage.py migrate`
Anda bisa langsung menggunakannya dengan `runserver` atau anda bisa menge-testnya dahulu
`./manage.py test`

### Requirements
Seingat saya, hanya :
- Django == 1.9 
- Python 3
- Selenium (`pip install selenium`)

### TODO
- [x] Functional Testing
- [x] Memperbaiki Template, ketika anda menggunakan ini secara langsung, template kosong, bisa anda lihat di templates.
- [ ] refactor view menggunakan CBV Class Based View

### Lain lain
Ini adalah projek latihan, anda bisa mempelajari, ikut memberikan kontribusi juga berupa saran penulisan kode yang baik atau penggunaan metode yang lebih baik, ini sangat terbuka. Dan saya sangat berterima kasih.
