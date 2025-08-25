#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes para a Calculadora de Rede
Suite de testes para validar todas as funcionalidades

Autor: Rodrigo Viana - https://rodrigoviana.dev.br
Versão: 1.0 - 23.08.2025
"""

import unittest
import sys
import os

# Adiciona o diretório atual ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from network_calculator import NetworkCalculator


class TestNetworkCalculator(unittest.TestCase):
    """Classe de testes para NetworkCalculator."""
    
    def setUp(self):
        """Configura o ambiente de teste."""
        self.calc = NetworkCalculator()
    
    def test_validate_ip_valid(self):
        """Testa validação de IPs válidos."""
        valid_ips = [
            "192.168.1.1",
            "10.0.0.1",
            "172.16.0.1",
            "8.8.8.8",
            "127.0.0.1"
        ]
        
        for ip in valid_ips:
            with self.subTest(ip=ip):
                self.assertTrue(self.calc.validate_ip(ip), f"IP {ip} deveria ser válido")
    
    def test_validate_ip_invalid(self):
        """Testa validação de IPs inválidos."""
        invalid_ips = [
            "256.1.1.1",
            "192.168.1",
            "192.168.1.1.1",
            "abc.def.ghi.jkl",
            "192.168.-1.1",
            ""
        ]
        
        for ip in invalid_ips:
            with self.subTest(ip=ip):
                self.assertFalse(self.calc.validate_ip(ip), f"IP {ip} deveria ser inválido")
    
    def test_validate_network_valid(self):
        """Testa validação de redes válidas."""
        valid_networks = [
            "192.168.1.0/24",
            "10.0.0.0/8",
            "172.16.0.0/12",
            "192.168.1.0/30",
            "0.0.0.0/0"
        ]
        
        for network in valid_networks:
            with self.subTest(network=network):
                self.assertTrue(self.calc.validate_network(network), 
                              f"Rede {network} deveria ser válida")
    
    def test_validate_network_invalid(self):
        """Testa validação de redes inválidas."""
        invalid_networks = [
            "192.168.1.0/33",
            "256.1.1.0/24",
            "192.168.1.0/-1",
            "192.168.1.0",
            "abc.def.ghi.jkl/24"
        ]
        
        for network in invalid_networks:
            with self.subTest(network=network):
                self.assertFalse(self.calc.validate_network(network), 
                               f"Rede {network} deveria ser inválida")
    
    def test_cidr_to_netmask(self):
        """Testa conversão de CIDR para máscara."""
        test_cases = [
            (24, "255.255.255.0"),
            (16, "255.255.0.0"),
            (8, "255.0.0.0"),
            (30, "255.255.255.252"),
            (0, "0.0.0.0"),
            (32, "255.255.255.255")
        ]
        
        for cidr, expected_mask in test_cases:
            with self.subTest(cidr=cidr):
                result = self.calc.cidr_to_netmask(cidr)
                self.assertEqual(result, expected_mask, 
                               f"CIDR /{cidr} deveria resultar em {expected_mask}")
    
    def test_cidr_to_netmask_invalid(self):
        """Testa conversão de CIDR inválido."""
        invalid_cidrs = [-1, 33, 100]
        
        for cidr in invalid_cidrs:
            with self.subTest(cidr=cidr):
                with self.assertRaises(ValueError):
                    self.calc.cidr_to_netmask(cidr)
    
    def test_netmask_to_cidr(self):
        """Testa conversão de máscara para CIDR."""
        test_cases = [
            ("255.255.255.0", 24),
            ("255.255.0.0", 16),
            ("255.0.0.0", 8),
            ("255.255.255.252", 30),
            ("0.0.0.0", 0),
            ("255.255.255.255", 32)
        ]
        
        for mask, expected_cidr in test_cases:
            with self.subTest(mask=mask):
                result = self.calc.netmask_to_cidr(mask)
                self.assertEqual(result, expected_cidr, 
                               f"Máscara {mask} deveria resultar em /{expected_cidr}")
    
    def test_calculate_network_info(self):
        """Testa cálculo de informações da rede."""
        network = "192.168.1.0/24"
        info = self.calc.calculate_network_info(network)
        
        expected_info = {
            'rede': '192.168.1.0',
            'mascara_cidr': '/24',
            'mascara_decimal': '255.255.255.0',
            'broadcast': '192.168.1.255',
            'primeiro_host': '192.168.1.1',
            'ultimo_host': '192.168.1.254',
            'total_hosts': '254',
            'total_enderecos': '256',
            'classe': 'C',
            'tipo': 'Privada'
        }
        
        for key, expected_value in expected_info.items():
            with self.subTest(key=key):
                self.assertEqual(info[key], expected_value, 
                               f"Campo {key} deveria ser {expected_value}")
    
    def test_subnet_network(self):
        """Testa divisão de rede em sub-redes."""
        network = "192.168.1.0/24"
        num_subnets = 4
        
        subnets = self.calc.subnet_network(network, num_subnets)
        
        # Verifica se retornou o número correto de sub-redes
        self.assertEqual(len(subnets), num_subnets)
        
        # Verifica a primeira sub-rede
        first_subnet = subnets[0]
        self.assertEqual(first_subnet['rede'], '192.168.1.0')
        self.assertEqual(first_subnet['cidr'], '/26')
        self.assertEqual(first_subnet['hosts_disponiveis'], '62')
    
    def test_ip_in_network(self):
        """Testa verificação se IP pertence à rede."""
        network = "192.168.1.0/24"
        
        # IPs que pertencem à rede
        valid_ips = ["192.168.1.1", "192.168.1.100", "192.168.1.254"]
        for ip in valid_ips:
            with self.subTest(ip=ip):
                self.assertTrue(self.calc.ip_in_network(ip, network), 
                              f"IP {ip} deveria pertencer à rede {network}")
        
        # IPs que não pertencem à rede
        invalid_ips = ["192.168.2.1", "10.0.0.1", "172.16.0.1"]
        for ip in invalid_ips:
            with self.subTest(ip=ip):
                self.assertFalse(self.calc.ip_in_network(ip, network), 
                                f"IP {ip} não deveria pertencer à rede {network}")
    
    def test_calculate_vlsm(self):
        """Testa cálculo de VLSM."""
        network = "192.168.1.0/24"
        host_requirements = [50, 25, 10]
        
        vlsm_subnets = self.calc.calculate_vlsm(network, host_requirements)
        
        # Verifica se retornou o número correto de sub-redes
        self.assertEqual(len(vlsm_subnets), len(host_requirements))
        
        # Verifica se as sub-redes foram ordenadas corretamente
        for i, subnet in enumerate(vlsm_subnets):
            self.assertEqual(subnet['ordem_original'], i + 1)
            self.assertEqual(subnet['hosts_solicitados'], host_requirements[i])
    
    def test_get_ip_class(self):
        """Testa determinação da classe do IP."""
        test_cases = [
            ("10.0.0.1", "A"),
            ("172.16.0.1", "B"),
            ("192.168.1.1", "C"),
            ("224.0.0.1", "D (Multicast)"),
            ("240.0.0.1", "E (Experimental)")
        ]
        
        for ip, expected_class in test_cases:
            with self.subTest(ip=ip):
                result = self.calc._get_ip_class(ip)
                self.assertEqual(result, expected_class, 
                               f"IP {ip} deveria ser classe {expected_class}")
    
    def test_is_private(self):
        """Testa verificação de IP privado."""
        import ipaddress
        
        # IPs privados
        private_ips = ["10.0.0.1", "172.16.0.1", "192.168.1.1"]
        for ip in private_ips:
            with self.subTest(ip=ip):
                ip_obj = ipaddress.IPv4Address(ip)
                self.assertTrue(self.calc._is_private(ip_obj), 
                              f"IP {ip} deveria ser privado")
        
        # IPs públicos
        public_ips = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
        for ip in public_ips:
            with self.subTest(ip=ip):
                ip_obj = ipaddress.IPv4Address(ip)
                self.assertFalse(self.calc._is_private(ip_obj), 
                                f"IP {ip} deveria ser público")


class TestIntegration(unittest.TestCase):
    """Testes de integração."""
    
    def setUp(self):
        """Configura o ambiente de teste."""
        self.calc = NetworkCalculator()
    
    def test_complete_workflow(self):
        """Testa um fluxo completo de uso."""
        # 1. Validar rede
        network = "10.0.0.0/8"
        self.assertTrue(self.calc.validate_network(network))
        
        # 2. Calcular informações da rede
        info = self.calc.calculate_network_info(network)
        self.assertEqual(info['classe'], 'A')
        self.assertEqual(info['tipo'], 'Privada')
        
        # 3. Dividir em sub-redes
        subnets = self.calc.subnet_network(network, 4)
        self.assertEqual(len(subnets), 4)
        
        # 4. Verificar se um IP pertence à rede original
        test_ip = "10.1.1.1"
        self.assertTrue(self.calc.ip_in_network(test_ip, network))
        
        # 5. Verificar se o IP pertence a uma das sub-redes
        belongs_to_subnet = any(
            self.calc.ip_in_network(test_ip, f"{subnet['rede']}{subnet['cidr']}")
            for subnet in subnets
        )
        self.assertTrue(belongs_to_subnet)


def run_tests():
    """Executa todos os testes."""
    print("="*70)
    print("           EXECUTANDO TESTES DA CALCULADORA DE REDE")
    print("="*70)
    
    # Cria a suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adiciona os testes
    suite.addTests(loader.loadTestsFromTestCase(TestNetworkCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Executa os testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Mostra o resumo
    print("\n" + "="*70)
    print("                        RESUMO DOS TESTES")
    print("="*70)
    print(f"Testes executados: {result.testsRun}")
    print(f"Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Falhas: {len(result.failures)}")
    print(f"Erros: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FALHAS:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError: ')[-1].split('\n')[0]}")
    
    if result.errors:
        print("\n❌ ERROS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\n')[-2]}")
    
    if result.wasSuccessful():
        print("\n✅ TODOS OS TESTES PASSARAM!")
    else:
        print("\n❌ ALGUNS TESTES FALHARAM!")
    
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)