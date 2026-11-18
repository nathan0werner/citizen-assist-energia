"""Testes automáticos: cálculos conferidos à mão e respostas do assistente.

Uso:  python -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from energia import calculos as c  # noqa: E402
from energia.alternativas import comparar, recomendar  # noqa: E402
from energia.assistente import AssistenteEnergia, detectar_intencao, extrair_dados  # noqa: E402


class TestCalculos(unittest.TestCase):
    def test_energia_potencia_tempo(self):
        # 5.500 W por 1 h = 5,5 kWh
        self.assertAlmostEqual(c.energia_kwh(5500, 1), 5.5)

    def test_chuveiro_cenario_base(self):
        # 4 pessoas × 8 min × 30 dias = 16 h; 5,5 kW × 16 h = 88 kWh
        self.assertAlmostEqual(c.chuveiro_kwh_mes(c.Perfil()), 88.0)

    def test_potencia_media(self):
        self.assertAlmostEqual(c.potencia_media_w(5500, 3200, 6), 4350)

    def test_delta_t(self):
        # ΔT = 5500 / (0,05 kg/s × 4186) ≈ 26,3 °C
        self.assertAlmostEqual(c.aumento_temperatura_c(5500, 3.0), 26.28, places=1)

    def test_conta_minimo_disponibilidade(self):
        p = c.Perfil(tarifa_kwh=1.0, custo_disponibilidade_kwh=50)
        self.assertEqual(c.conta_mensal(20, p), 50)
        self.assertEqual(c.conta_mensal(200, p), 200)

    def test_conta_tarifa_social(self):
        p = c.Perfil(tarifa_kwh=1.0, tarifa_social=True)
        self.assertEqual(c.conta_mensal(70, p), 0)
        self.assertEqual(c.conta_mensal(100, p), 20)

    def test_fv_geracao(self):
        # 1 kWp × 4,6 × 0,75 × 30 = 103,5 kWh/mês
        self.assertAlmostEqual(c.fv_geracao_kwh_mes(1.0), 103.5)

    def test_fv_dimensionamento_inteiro_de_modulos(self):
        kwp, modulos = c.fv_dimensionar_kwp(88)
        self.assertEqual(modulos, 2)
        self.assertAlmostEqual(kwp, 1.1)

    def test_payback(self):
        self.assertAlmostEqual(c.payback_anos(1000, 250), 4)
        self.assertEqual(c.payback_anos(1000, 0), float("inf"))


class TestAlternativas(unittest.TestCase):
    def setUp(self):
        self.res = comparar(c.Perfil())

    def test_mesma_necessidade(self):
        # hábitos e solar reduzem a energia do banho; nenhuma alternativa aumenta a conta
        self.assertLess(self.res["A1"].kwh_chuveiro_mes, self.res["A0"].kwh_chuveiro_mes)
        self.assertLess(self.res["A2"].kwh_chuveiro_mes, self.res["A0"].kwh_chuveiro_mes)
        for r in self.res.values():
            self.assertGreaterEqual(r.economia_r_mes, 0)

    def test_valores_cenario_base(self):
        self.assertAlmostEqual(self.res["A1"].kwh_chuveiro_mes, 43.5)
        self.assertAlmostEqual(self.res["A2"].kwh_chuveiro_mes, 26.4)
        self.assertAlmostEqual(self.res["A1"].economia_r_mes, 44.5 * 1.09)

    def test_pelo_menos_uma_renovavel(self):
        self.assertTrue(any(r.renovavel for r in self.res.values()))

    def test_recomendacao_comeca_por_habitos(self):
        self.assertEqual(recomendar(self.res, c.Perfil())[0], "A1")

    def test_tarifa_social_poe_fv_por_ultimo(self):
        p = c.Perfil(tarifa_social=True)
        self.assertEqual(recomendar(comparar(p), p)[-1], "A3")


class TestAssistente(unittest.TestCase):
    def test_intencoes(self):
        casos = {
            "quanto gasta meu chuveiro?": "chuveiro",
            "vale a pena aquecedor solar?": "aquecedor_solar",
            "e placa solar?": "fotovoltaico",
            "compare as opções": "comparar",
            "dicas para o banho": "habitos",
            "como funciona a tarifa social?": "tarifa_social",
            "quais as fontes?": "fontes",
            "limitações": "limitacoes",
        }
        for msg, esperado in casos.items():
            self.assertEqual(detectar_intencao(msg), esperado, msg)

    def test_extrai_dados(self):
        p = c.Perfil()
        extrair_dados("somos 3 pessoas, banho de 10 minutos, chuveiro 6,8 kW, conta de R$ 150 com 160 kWh", p)
        self.assertEqual(p.pessoas, 3)
        self.assertEqual(p.minutos_banho, 10)
        self.assertEqual(p.potencia_inverno_w, 6800)
        self.assertEqual(p.consumo_total_kwh_mes, 160)
        self.assertAlmostEqual(p.tarifa_kwh, 150 / 160)

    def test_kwh_nao_vira_potencia(self):
        p = c.Perfil()
        extrair_dados("consumo 200 kWh", p)
        self.assertEqual(p.potencia_inverno_w, 5500)

    def test_resposta_tem_fontes_e_aviso(self):
        r = AssistenteEnergia().responder("compare as alternativas")
        self.assertIn("Fontes", r)
        self.assertIn("Não são garantia", r)

    def test_resposta_usa_numeros_da_analise(self):
        bot = AssistenteEnergia()
        esperado = comparar(bot.perfil)["A1"].economia_r_mes
        self.assertIn(f"{esperado:.2f}".replace(".", ","), bot.responder("dicas para economizar no banho"))

    def test_reiniciar(self):
        bot = AssistenteEnergia()
        bot.responder("somos 2 pessoas")
        bot.responder("reiniciar")
        self.assertEqual(bot.perfil.pessoas, 4)


if __name__ == "__main__":
    unittest.main()
