from django.test import SimpleTestCase


class VistaPrincipal(SimpleTestCase):
    def test_get_muestra_los_dos_formularios(self):
        r = self.client.get("/")
        self.assertContains(r, "Conversor de sistemas numéricos")
        self.assertContains(r, "Analizador de caracteres")

    def test_conversion_valida_en_pantalla(self):
        r = self.client.post("/", {"accion": "numero", "n-numero": "FF", "n-base": "16"})
        self.assertContains(r, "11111111")
        self.assertContains(r, "Bits significativos")

    def test_error_en_pantalla_por_digito_invalido(self):
        r = self.client.post("/", {"accion": "numero", "n-numero": "12", "n-base": "2"})
        self.assertContains(r, "no válido(s) para base 2")
        self.assertNotContains(r, "Bits significativos")

    def test_error_en_pantalla_por_campo_vacio(self):
        r = self.client.post("/", {"accion": "numero", "n-numero": "", "n-base": "10"})
        self.assertContains(r, "no puede estar vacío")

    def test_texto_con_enie_en_pantalla(self):
        r = self.client.post("/", {"accion": "texto", "t-texto": "año"})
        self.assertContains(r, "U+00F1")
        self.assertContains(r, "C3 B1")
