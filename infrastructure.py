#!/usr/bin/env python3

from troposphere import Ref, GetAtt, Join
import json
import sys
import os

from fl_aws.blueprints.vpc import VPC


class APIVPC(VPC):

    PROJECT = 'APIVPC'
    ENVIRONMENT = os.environ['ENVIRONMENT']

    BASE_VPC_CIDR = '10.{0}.0.0/16'

    SECOND_OCTET = 'SECOND_OCTET'
    BANKSTATEMENTS_API = 'SharedBankStatementsAPI'
    APPLY_API = 'SharedApplyAPI'
    PEERING_CONFIG = 'PEERING_CONFIG'
    PEERING_DESTINATION_VPC_CONFIG = 'PEERING_DESTINATION_VPC_CONFIG'
    PEERING_DESTINATION_RANGE_CONFIG = 'PEERING_DESTINATION_RANGE_CONFIG'
    PEERING_DESTINATION_ROUTE_TABLES_CONFIG = 'PEERING_DESTINATION_ROUTE_TABLES_CONFIG'

    VPC_SECOND_OCTET = VPC.get_second_octet(PROJECT, ENVIRONMENT)

    PROJECTS = {
        BANKSTATEMENTS_API: {
            SECOND_OCTET: VPC.get_second_octet(BANKSTATEMENTS_API, ENVIRONMENT),
            PEERING_CONFIG: {
                PEERING_DESTINATION_VPC_CONFIG: {
                    'FAWSORG': {
                        'STG': 'vpc-5e744b3a',
                        'PRD': 'vpc-5e744b3a',
                    }
                },
                PEERING_DESTINATION_RANGE_CONFIG: {
                    'FAWSORG': {
                        'STG': '10.173.0.0/22',
                        'PRD': '10.173.0.0/22',
                    }
                },
                PEERING_DESTINATION_ROUTE_TABLES_CONFIG: {
                    'FAWSORG': {
                        'STG': ['rtb-076b4660', 'rtb-05c0db8b6136b48a3'],
                        'PRD': ['rtb-076b4660', 'rtb-2e847549'],
                    }
                }
            }
        },
        APPLY_API: {
            SECOND_OCTET: VPC.get_second_octet(APPLY_API, ENVIRONMENT),
        }
    }

    CIDR = BASE_VPC_CIDR.format(VPC_SECOND_OCTET)
    PUBLIC_NAT_SUBNETS = {
        'NATA': '10.{0}.0.0/27'.format(VPC_SECOND_OCTET),
        'NATB': '10.{0}.0.32/27'.format(VPC_SECOND_OCTET),
    }
    PUBLIC_SUBNETS = {}
    PRIVATE_SUBNETS = {}

    for project, config in PROJECTS.items():
        second_octet = config[SECOND_OCTET]
        PRIVATE_SUBNETS.update({'{0}A'.format(project): '10.{0}.10.0/24'.format(second_octet)})
        PRIVATE_SUBNETS.update({'{0}B'.format(project): '10.{0}.11.0/24'.format(second_octet)})
        PROJECTS[project].update({'CIDR': BASE_VPC_CIDR.format(second_octet)})

    INTERFACE_SUBNETS = {
        'InterfaceA': '10.{0}.3.0/25'.format(VPC_SECOND_OCTET),
        'InterfaceB': '10.{0}.3.128/25'.format(VPC_SECOND_OCTET),
    }

    def add_components(self):

        """ Peering Connection Resources """
        for project, config in self.PROJECTS.items():
            try:
                peering_config = config[self.PEERING_CONFIG]
                for vpc_name, environment in peering_config[self.PEERING_DESTINATION_RANGE_CONFIG].items():
                    if self.ENVIRONMENT not in environment:
                        continue

                    """ Peering Connection """
                    peering_connection = self.ec2_helper.create_peering_connection(
                        vpc=Ref(self.vpc),
                        peer_vpc=peering_config[self.PEERING_DESTINATION_VPC_CONFIG][vpc_name][self.ENVIRONMENT],
                        peer_name='{0}-to-{1}-{2}'.format(self.PROJECT, vpc_name, self.ENVIRONMENT),
                        name_prefix=vpc_name
                    )

                    """ Routes to Peering Connection for this VPC """
                    for route_table in self.private_route_tables:
                        self.ec2_helper.create_route(
                            name_prefix='{0}{1}'.format(vpc_name, route_table.title),
                            RouteTableId=Ref(route_table),
                            DestinationCidrBlock=peering_config[self.PEERING_DESTINATION_RANGE_CONFIG][vpc_name][self.ENVIRONMENT],
                            VpcPeeringConnectionId=Ref(peering_connection))

                    """ Routes to Peering Connection for peer VPC CIDR """
                    count = 0
                    for route_table in peering_config[self.PEERING_DESTINATION_ROUTE_TABLES_CONFIG][vpc_name][self.ENVIRONMENT]:
                        count += 1
                        # Additional project CIDR
                        self.ec2_helper.create_route(
                            name_prefix='{0}{1}PeerVPC'.format(project, count),
                            RouteTableId=route_table,
                            DestinationCidrBlock=config['CIDR'],
                            VpcPeeringConnectionId=Ref(peering_connection))

            except Exception as e:
                pass


if __name__ == '__main__':
    api_vpc = APIVPC()
    api_vpc.init_template()
    api_vpc.add_components()
    print(api_vpc.t.to_json())
