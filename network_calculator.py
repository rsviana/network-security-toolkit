#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora de Rede Completa
Sistema para cálculos e análises de redes IP

Autor: Rodrigo Viana - https://rodrigoviana.dev.br
Versão: 1.0 - 23.08.2025
"""

import ipaddress
import socket
import struct
from typing import List, Dict, Tuple, Optional
import re


class NetworkCalculator:
    """Classe principal para cálculos de rede."""
    
    def __init__(self):
        """Inicializa a calculadora de rede."""
        self.private_ranges = [
            ipaddress.IPv4Network('10.0.0.0/8'),
            ipaddress.IPv4Network('172.16.0.0/12'),
            ipaddress.IPv4Network('192.168.0.0/16')
        ]
    
    def validate_ip(self, ip: str) -> bool:
        """Valida se um endereço IP é válido.
        
        Args:
            ip (str): Endereço IP a ser validado
            
        Returns:
            bool: True se válido, False caso contrário
        """
        try:
            ipaddress.IPv4Address(ip)
            return True
        except ipaddress.AddressValueError:
            return False
    
    def validate_network(self, network: str) -> bool:
        """Valida se uma rede é válida.
        
        Args:
            network (str): Rede no formato CIDR (ex: 192.168.1.0/24)
            
        Returns:
            bool: True se válida, False caso contrário
        """
        try:
            ipaddress.IPv4Network(network, strict=False)
            return True
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
            return False
    
    def cidr_to_netmask(self, cidr: int) -> str:
        """Converte notação CIDR para máscara de sub-rede.
        
        Args:
            cidr (int): Valor CIDR (0-32)
            
        Returns:
            str: Máscara de sub-rede em formato decimal pontuado
        """
        if not 0 <= cidr <= 32:
            raise ValueError("CIDR deve estar entre 0 e 32")
        
        mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
        return socket.inet_ntoa(struct.pack('>I', mask))
    
    def netmask_to_cidr(self, netmask: str) -> int:
        """Converte máscara de sub-rede para notação CIDR.
        
        Args:
            netmask (str): Máscara de sub-rede em formato decimal pontuado
            
        Returns:
            int: Valor CIDR
        """
        try:
            return ipaddress.IPv4Network(f'0.0.0.0/{netmask}').prefixlen
        except ipaddress.NetmaskValueError:
            raise ValueError("Máscara de sub-rede inválida")
    
    def calculate_network_info(self, network: str) -> Dict[str, str]:
        """Calcula informações completas de uma rede.
        
        Args:
            network (str): Rede no formato CIDR
            
        Returns:
            Dict[str, str]: Dicionário com informações da rede
        """
        try:
            net = ipaddress.IPv4Network(network, strict=False)
            
            info = {
                'rede': str(net.network_address),
                'mascara_cidr': f'/{net.prefixlen}',
                'mascara_decimal': str(net.netmask),
                'broadcast': str(net.broadcast_address),
                'primeiro_host': str(net.network_address + 1),
                'ultimo_host': str(net.broadcast_address - 1),
                'total_hosts': str(net.num_addresses - 2),
                'total_enderecos': str(net.num_addresses),
                'classe': self._get_ip_class(str(net.network_address)),
                'tipo': 'Privada' if self._is_private(net.network_address) else 'Pública'
            }
            
            return info
            
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError) as e:
            raise ValueError(f"Rede inválida: {e}")
    
    def subnet_network(self, network: str, num_subnets: int) -> List[Dict[str, str]]:
        """Divide uma rede em sub-redes.
        
        Args:
            network (str): Rede original no formato CIDR
            num_subnets (int): Número de sub-redes desejadas
            
        Returns:
            List[Dict[str, str]]: Lista com informações das sub-redes
        """
        try:
            net = ipaddress.IPv4Network(network, strict=False)
            
            # Calcula quantos bits são necessários para o número de sub-redes
            import math
            bits_needed = math.ceil(math.log2(num_subnets))
            new_prefix = net.prefixlen + bits_needed
            
            if new_prefix > 32:
                raise ValueError("Não é possível criar tantas sub-redes")
            
            subnets = list(net.subnets(new_prefix=new_prefix))
            
            result = []
            for i, subnet in enumerate(subnets[:num_subnets]):
                subnet_info = {
                    'subnet_id': i + 1,
                    'rede': str(subnet.network_address),
                    'cidr': f'/{subnet.prefixlen}',
                    'mascara': str(subnet.netmask),
                    'broadcast': str(subnet.broadcast_address),
                    'primeiro_host': str(subnet.network_address + 1),
                    'ultimo_host': str(subnet.broadcast_address - 1),
                    'hosts_disponiveis': str(subnet.num_addresses - 2)
                }
                result.append(subnet_info)
            
            return result
            
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError) as e:
            raise ValueError(f"Erro ao dividir rede: {e}")
    
    def supernet_networks(self, networks: List[str]) -> Optional[str]:
        """Calcula a super-rede de uma lista de redes.
        
        Args:
            networks (List[str]): Lista de redes no formato CIDR
            
        Returns:
            Optional[str]: Super-rede ou None se não for possível
        """
        try:
            net_objects = [ipaddress.IPv4Network(net, strict=False) for net in networks]
            supernet = ipaddress.collapse_addresses(net_objects)
            
            # Se todas as redes podem ser resumidas em uma única super-rede
            supernet_list = list(supernet)
            if len(supernet_list) == 1:
                return str(supernet_list[0])
            else:
                return None
                
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
            return None
    
    def ip_in_network(self, ip: str, network: str) -> bool:
        """Verifica se um IP pertence a uma rede.
        
        Args:
            ip (str): Endereço IP
            network (str): Rede no formato CIDR
            
        Returns:
            bool: True se o IP pertence à rede
        """
        try:
            ip_obj = ipaddress.IPv4Address(ip)
            net_obj = ipaddress.IPv4Network(network, strict=False)
            return ip_obj in net_obj
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
            return False
    
    def calculate_vlsm(self, network: str, host_requirements: List[int]) -> List[Dict[str, str]]:
        """Calcula VLSM (Variable Length Subnet Masking).
        
        Args:
            network (str): Rede original
            host_requirements (List[int]): Lista com número de hosts necessários
            
        Returns:
            List[Dict[str, str]]: Lista com sub-redes VLSM
        """
        try:
            net = ipaddress.IPv4Network(network, strict=False)
            
            # Ordena os requisitos em ordem decrescente
            sorted_requirements = sorted(enumerate(host_requirements), 
                                       key=lambda x: x[1], reverse=True)
            
            result = []
            current_network = net
            
            for original_index, hosts_needed in sorted_requirements:
                # Calcula o prefixo necessário
                import math
                bits_for_hosts = math.ceil(math.log2(hosts_needed + 2))  # +2 para rede e broadcast
                new_prefix = 32 - bits_for_hosts
                
                if new_prefix < current_network.prefixlen:
                    raise ValueError(f"Não há espaço suficiente para {hosts_needed} hosts")
                
                # Encontra a primeira sub-rede disponível
                subnet = None
                for possible_subnet in current_network.subnets(new_prefix=new_prefix):
                    subnet = possible_subnet
                    break
                
                if subnet is None:
                    raise ValueError("Não foi possível alocar sub-rede")
                
                subnet_info = {
                    'ordem_original': original_index + 1,
                    'hosts_solicitados': hosts_needed,
                    'rede': str(subnet.network_address),
                    'cidr': f'/{subnet.prefixlen}',
                    'mascara': str(subnet.netmask),
                    'broadcast': str(subnet.broadcast_address),
                    'primeiro_host': str(subnet.network_address + 1),
                    'ultimo_host': str(subnet.broadcast_address - 1),
                    'hosts_disponiveis': str(subnet.num_addresses - 2)
                }
                result.append(subnet_info)
                
                # Atualiza a rede atual para excluir a sub-rede alocada
                remaining_networks = list(current_network.address_exclude(subnet))
                if remaining_networks:
                    current_network = remaining_networks[0]
                else:
                    break
            
            # Reordena o resultado pela ordem original
            result.sort(key=lambda x: x['ordem_original'])
            return result
            
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError) as e:
            raise ValueError(f"Erro no cálculo VLSM: {e}")
    
    def _get_ip_class(self, ip: str) -> str:
        """Determina a classe de um endereço IP.
        
        Args:
            ip (str): Endereço IP
            
        Returns:
            str: Classe do IP (A, B, C, D, E)
        """
        try:
            ip_obj = ipaddress.IPv4Address(ip)
            first_octet = int(str(ip_obj).split('.')[0])
            
            if 1 <= first_octet <= 126:
                return 'A'
            elif 128 <= first_octet <= 191:
                return 'B'
            elif 192 <= first_octet <= 223:
                return 'C'
            elif 224 <= first_octet <= 239:
                return 'D (Multicast)'
            elif 240 <= first_octet <= 255:
                return 'E (Experimental)'
            else:
                return 'Indefinida'
        except:
            return 'Inválida'
    
    def _is_private(self, ip) -> bool:
        """Verifica se um IP é privado.
        
        Args:
            ip: Objeto IPv4Address
            
        Returns:
            bool: True se for IP privado
        """
        for private_range in self.private_ranges:
            if ip in private_range:
                return True
        return False
    
    def get_network_summary(self, network: str) -> str:
        """Gera um resumo formatado das informações da rede.
        
        Args:
            network (str): Rede no formato CIDR
            
        Returns:
            str: Resumo formatado
        """
        try:
            info = self.calculate_network_info(network)
            
            summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                    INFORMAÇÕES DA REDE                      ║
╠══════════════════════════════════════════════════════════════╣
║ Rede:              {info['rede']:<30} ║
║ CIDR:              {info['mascara_cidr']:<30} ║
║ Máscara:           {info['mascara_decimal']:<30} ║
║ Broadcast:         {info['broadcast']:<30} ║
║ Primeiro Host:     {info['primeiro_host']:<30} ║
║ Último Host:       {info['ultimo_host']:<30} ║
║ Total de Hosts:    {info['total_hosts']:<30} ║
║ Total Endereços:   {info['total_enderecos']:<30} ║
║ Classe:            {info['classe']:<30} ║
║ Tipo:              {info['tipo']:<30} ║
╚══════════════════════════════════════════════════════════════╝
            """
            
            return summary.strip()
            
        except ValueError as e:
            return f"Erro: {e}"


if __name__ == "__main__":
    # Exemplo de uso
    calc = NetworkCalculator()
    
    # Teste básico
    print("=== CALCULADORA DE REDE ===")
    print("\nTeste com rede 192.168.1.0/24:")
    print(calc.get_network_summary("192.168.1.0/24"))
    
    print("\n=== DIVISÃO EM SUB-REDES ===")
    subnets = calc.subnet_network("192.168.1.0/24", 4)
    for subnet in subnets:
        print(f"Sub-rede {subnet['subnet_id']}: {subnet['rede']}{subnet['cidr']} - Hosts: {subnet['hosts_disponiveis']}")