#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface de Linha de Comando para Calculadora de Rede
Interface interativa para usar todas as funcionalidades da calculadora

Autor: Rodrigo Viana - https://rodrigoviana.dev.br
Versão: 1.0 - 23.08.2025
"""

import sys
import os
from typing import List
from network_calculator import NetworkCalculator


class NetworkCalculatorCLI:
    """Interface de linha de comando para a calculadora de rede."""
    
    def __init__(self):
        """Inicializa a interface CLI."""
        self.calculator = NetworkCalculator()
        self.running = True
    
    def display_banner(self):
        """Exibe o banner inicial do programa."""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          CALCULADORA DE REDE                                 ║
║                     Sistema Completo para Cálculos de Rede                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def display_menu(self):
        """Exibe o menu principal."""
        menu = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                              MENU PRINCIPAL                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  1. Calcular informações de rede                                           │
│  2. Converter CIDR para máscara decimal                                    │
│  3. Converter máscara decimal para CIDR                                    │
│  4. Dividir rede em sub-redes (FLSM)                                       │
│  5. Calcular VLSM (Variable Length Subnet Masking)                         │
│  6. Verificar se IP pertence a uma rede                                    │
│  7. Calcular super-rede                                                    │
│  8. Validar endereço IP                                                    │
│  9. Validar rede                                                           │
│  0. Sair                                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
        """
        print(menu)
    
    def get_user_input(self, prompt: str, input_type: str = "string") -> any:
        """Obtém entrada do usuário com validação.
        
        Args:
            prompt (str): Mensagem para o usuário
            input_type (str): Tipo de entrada esperada
            
        Returns:
            any: Valor inserido pelo usuário
        """
        while True:
            try:
                user_input = input(f"\n{prompt}: ").strip()
                
                if input_type == "int":
                    return int(user_input)
                elif input_type == "list_int":
                    return [int(x.strip()) for x in user_input.split(',')]
                elif input_type == "list_str":
                    return [x.strip() for x in user_input.split(',')]
                else:
                    return user_input
                    
            except ValueError:
                print("❌ Entrada inválida. Tente novamente...")
            except KeyboardInterrupt:
                print("\n\n👋 Programa interrompido pelo usuário!")
                sys.exit(0)
    
    def option_1_network_info(self):
        """Opção 1: Calcular informações de rede."""
        print("\n" + "="*60)
        print("           CALCULAR INFORMAÇÕES DE REDE")
        print("="*60)
        
        network = self.get_user_input("Digite a rede (ex: 192.168.1.0/24)")
        
        try:
            print(self.calculator.get_network_summary(network))
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def option_2_cidr_to_netmask(self):
        """Opção 2: Converter CIDR para máscara decimal."""
        print("\n" + "="*60)
        print("        CONVERTER CIDR PARA MÁSCARA DECIMAL")
        print("="*60)
        
        cidr = self.get_user_input("Digite o valor CIDR (0-32)", "int")
        
        try:
            netmask = self.calculator.cidr_to_netmask(cidr)
            print(f"\n✅ CIDR /{cidr} = Máscara {netmask}")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def option_3_netmask_to_cidr(self):
        """Opção 3: Converter máscara decimal para CIDR."""
        print("\n" + "="*60)
        print("        CONVERTER MÁSCARA DECIMAL PARA CIDR")
        print("="*60)
        
        netmask = self.get_user_input("Digite a máscara (ex: 255.255.255.0)")
        
        try:
            cidr = self.calculator.netmask_to_cidr(netmask)
            print(f"\n✅ Máscara {netmask} = CIDR /{cidr}")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def option_4_subnet_network(self):
        """Opção 4: Dividir rede em sub-redes."""
        print("\n" + "="*60)
        print("           DIVIDIR REDE EM SUB-REDES (FLSM)")
        print("="*60)
        
        network = self.get_user_input("Digite a rede (ex: 192.168.1.0/24)")
        num_subnets = self.get_user_input("Digite o número de sub-redes desejadas", "int")
        
        try:
            subnets = self.calculator.subnet_network(network, num_subnets)
            
            print(f"\n✅ Divisão da rede {network} em {num_subnets} sub-redes:")
            print("\n" + "─"*100)
            print(f"{'ID':<3} {'Rede':<18} {'CIDR':<6} {'Máscara':<15} {'Broadcast':<15} {'Hosts':<8}")
            print("─"*100)
            
            for subnet in subnets:
                print(f"{subnet['subnet_id']:<3} {subnet['rede']:<18} {subnet['cidr']:<6} "
                      f"{subnet['mascara']:<15} {subnet['broadcast']:<15} {subnet['hosts_disponiveis']:<8}")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def option_5_vlsm(self):
        """Opção 5: Calcular VLSM."""
        print("\n" + "="*60)
        print("              CALCULAR VLSM")
        print("="*60)
        
        network = self.get_user_input("Digite a rede (ex: 192.168.1.0/24)")
        print("\nDigite o número de hosts necessários para cada sub-rede.")
        print("Exemplo: 50,25,10,5 (separados por vírgula)")
        host_requirements = self.get_user_input("Requisitos de hosts", "list_int")
        
        try:
            vlsm_subnets = self.calculator.calculate_vlsm(network, host_requirements)
            
            print(f"\n✅ VLSM para a rede {network}:")
            print("\n" + "─"*110)
            print(f"{'Ordem':<6} {'Solicitado':<10} {'Rede':<18} {'CIDR':<6} {'Disponível':<10} {'Range de Hosts':<25}")
            print("─"*110)
            
            for subnet in vlsm_subnets:
                host_range = f"{subnet['primeiro_host']} - {subnet['ultimo_host']}"
                print(f"{subnet['ordem_original']:<6} {subnet['hosts_solicitados']:<10} "
                      f"{subnet['rede']:<18} {subnet['cidr']:<6} {subnet['hosts_disponiveis']:<10} "
                      f"{host_range:<25}")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def option_6_ip_in_network(self):
        """Opção 6: Verificar se IP pertence a uma rede."""
        print("\n" + "="*60)
        print("        VERIFICAR SE IP PERTENCE À REDE")
        print("="*60)
        
        ip = self.get_user_input("Digite o endereço IP")
        network = self.get_user_input("Digite a rede (ex: 192.168.1.0/24)")
        
        try:
            belongs = self.calculator.ip_in_network(ip, network)
            
            if belongs:
                print(f"\n✅ O IP {ip} PERTENCE à rede {network}")
            else:
                print(f"\n❌ O IP {ip} NÃO PERTENCE à rede {network}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def option_7_supernet(self):
        """Opção 7: Calcular super-rede."""
        print("\n" + "="*60)
        print("              CALCULAR SUPER-REDE")
        print("="*60)
        
        print("\nDigite as redes separadas por vírgula.")
        print("Exemplo: 192.168.1.0/26,192.168.1.64/26,192.168.1.128/26")
        networks_input = self.get_user_input("Redes", "list_str")
        
        try:
            supernet = self.calculator.supernet_networks(networks_input)
            
            if supernet:
                print(f"\n✅ Super-rede calculada: {supernet}")
                print("\nInformações da super-rede:")
                print(self.calculator.get_network_summary(supernet))
            else:
                print("\n❌ Não foi possível calcular uma super-rede única para essas redes.")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def option_8_validate_ip(self):
        """Opção 8: Validar endereço IP."""
        print("\n" + "="*60)
        print("            VALIDAR ENDEREÇO IP")
        print("="*60)
        
        ip = self.get_user_input("Digite o endereço IP")
        
        try:
            is_valid = self.calculator.validate_ip(ip)
            
            if is_valid:
                print(f"\n✅ O endereço IP {ip} é VÁLIDO")
                
                # Informações adicionais
                ip_class = self.calculator._get_ip_class(ip)
                print(f"   Classe: {ip_class}")
                
                import ipaddress
                ip_obj = ipaddress.IPv4Address(ip)
                is_private = self.calculator._is_private(ip_obj)
                print(f"   Tipo: {'Privado' if is_private else 'Público'}")
            else:
                print(f"\n❌ O endereço IP {ip} é INVÁLIDO")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def option_9_validate_network(self):
        """Opção 9: Validar rede."""
        print("\n" + "="*60)
        print("               VALIDAR REDE")
        print("="*60)
        
        network = self.get_user_input("Digite a rede (ex: 192.168.1.0/24)")
        
        try:
            is_valid = self.calculator.validate_network(network)
            
            if is_valid:
                print(f"\n✅ A rede {network} é VÁLIDA")
            else:
                print(f"\n❌ A rede {network} é INVÁLIDA")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def run(self):
        """Executa a interface principal."""
        self.display_banner()
        
        while self.running:
            try:
                self.display_menu()
                choice = self.get_user_input("\nEscolha uma opção", "int")
                
                if choice == 0:
                    print("\n👋 Obrigado por usar a Calculadora de Rede!")
                    self.running = False
                elif choice == 1:
                    self.option_1_network_info()
                elif choice == 2:
                    self.option_2_cidr_to_netmask()
                elif choice == 3:
                    self.option_3_netmask_to_cidr()
                elif choice == 4:
                    self.option_4_subnet_network()
                elif choice == 5:
                    self.option_5_vlsm()
                elif choice == 6:
                    self.option_6_ip_in_network()
                elif choice == 7:
                    self.option_7_supernet()
                elif choice == 8:
                    self.option_8_validate_ip()
                elif choice == 9:
                    self.option_9_validate_network()
                else:
                    print("❌ Opção inválida. Escolha um número de 0 a 9.")
                
                if choice != 0:
                    input("\n\nPressione Enter para continuar...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Programa interrompido pelo usuário.")
                break
            except Exception as e:
                print(f"❌ Erro inesperado: {e}")
                input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    cli = NetworkCalculatorCLI()
    cli.run()