#!/usr/bin/env python3

import json
import sys
import os

from troposphere import Ref, GetAtt, ImportValue

from fl_aws.blueprints.vpc import VPC


class APIVPC(VPC):

    PROJECT = 'APIVPC'
    ENVIRONMENT = os.environ['ENVIRONMENT']
    BASE_VPC_CIDR = '10.{0}.0.0/16'

    BANKSTATEMENTS_API = 'SharedBankStatementsAPI'
    NESTED_BANKSTATEMENTS_API = 'NestedBankStatementsAPI'
    APPLY_API = 'SharedApplyAPI'
    DATA_MOVER = 'SharedDataMover'
    OPPORTUNITY_FEEDER = 'SharedOpportunityFeeder'
    PROSPECTS_API = 'SharedProspectsAPI'
    ANALYTICS_PLATFORM = 'SharedAnalyticsPlatformAPI'
    ANALYTICS = 'NestedAnalytics'
    FORSIGHT_API = 'SharedForsightAPI'
    FRAUD_API = 'NestedFraudAPI'
    CREDIT_BUREAU_API = 'NestedCreditBureauAPI'
    NOTIFICATIONS_API = 'SharedNotificationsAPI'
    MILO_API = 'SharedMiloAPI'
    FORWARDLINE_DB = 'ForwardlineDB'
    FORWARDLINE_CODEBUILD = 'ForwardlineCodeBuild'
    NESTED_REPORT_API = 'NestedReportAPI'

    PROSPECTS_ELASTIC_SEARCH = 'ProspectsElasticsearch'

    SECOND_OCTET = 'SECOND_OCTET'
    PEERING_CONFIG = 'PEERING_CONFIG'
    PEERING_DESTINATION_VPC_CONFIG = 'PEERING_DESTINATION_VPC_CONFIG'
    PEERING_DESTINATION_RANGE_CONFIG = 'PEERING_DESTINATION_RANGE_CONFIG'
    PEERING_DESTINATION_ROUTE_TABLES_CONFIG = 'PEERING_DESTINATION_ROUTE_TABLES_CONFIG'
    PEERING_DESTINATION_NAME = 'PEERING_DESTINATION_NAME'
    PRIVATE_SUBNETS_CONFIG = 'PRIVATE_SUBNETS_CONFIG'
    PUBLIC_SUBNETS_CONFIG = 'PUBLIC_SUBNETS_CONFIG'
    PEERING_CONNECTION = 'PeeringConnection'

    VPC_SECOND_OCTET = VPC.get_second_octet(PROJECT, ENVIRONMENT)

    PROSPECTS_ELASTIC_SEARCH_CIDR = BASE_VPC_CIDR.format(VPC.get_second_octet(PROSPECTS_ELASTIC_SEARCH, ENVIRONMENT))

    NESTED_PROJECTS = {
        NESTED_BANKSTATEMENTS_API: {
            SECOND_OCTET: VPC.get_second_octet(NESTED_BANKSTATEMENTS_API, ENVIRONMENT),
            PEERING_CONFIG: {
                PEERING_DESTINATION_NAME: 'FAWSORG',
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
        NESTED_REPORT_API: {
            SECOND_OCTET: VPC.get_second_octet(NESTED_REPORT_API, ENVIRONMENT),
            PEERING_CONFIG: {
                PEERING_DESTINATION_NAME: 'FAWSORG',
                PEERING_DESTINATION_RANGE_CONFIG: {
                    'OVERVIEWDB': {
                        'STG': '10.173.2.128/27',
                        'PRD': '10.173.1.192/27',
                    }
                },
            }
        },
        ANALYTICS: {
            SECOND_OCTET: VPC.get_second_octet(ANALYTICS, ENVIRONMENT),
        },
        FRAUD_API: {
            SECOND_OCTET: VPC.get_second_octet(FRAUD_API, ENVIRONMENT),
            PRIVATE_SUBNETS_CONFIG: {
                '{0}A'.format(FRAUD_API): '10.{0}.10.0/24'.format(
                    VPC.get_second_octet(FRAUD_API, ENVIRONMENT)),
                '{0}B'.format(FRAUD_API): '10.{0}.11.0/24'.format(
                    VPC.get_second_octet(FRAUD_API, ENVIRONMENT)),
                '{0}RedisA'.format(FRAUD_API): '10.{0}.12.0/24'.format(
                    VPC.get_second_octet(FRAUD_API, ENVIRONMENT)),
                '{0}RedisB'.format(FRAUD_API): '10.{0}.13.0/24'.format(
                    VPC.get_second_octet(FRAUD_API, ENVIRONMENT)),
            }
        },
        CREDIT_BUREAU_API: {
            SECOND_OCTET: VPC.get_second_octet(CREDIT_BUREAU_API, ENVIRONMENT),
            PRIVATE_SUBNETS_CONFIG: {
                '{0}A'.format(CREDIT_BUREAU_API): '10.{0}.10.0/24'.format(
                    VPC.get_second_octet(CREDIT_BUREAU_API, ENVIRONMENT)),
                '{0}B'.format(CREDIT_BUREAU_API): '10.{0}.11.0/24'.format(
                    VPC.get_second_octet(CREDIT_BUREAU_API, ENVIRONMENT)),
                '{0}RedisA'.format(CREDIT_BUREAU_API): '10.{0}.12.0/24'.format(
                    VPC.get_second_octet(CREDIT_BUREAU_API, ENVIRONMENT)),
                '{0}RedisB'.format(CREDIT_BUREAU_API): '10.{0}.13.0/24'.format(
                    VPC.get_second_octet(CREDIT_BUREAU_API, ENVIRONMENT)),
            }
        },
    }

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
            PEERING_CONFIG: {
                PEERING_DESTINATION_VPC_CONFIG: {
                    PROSPECTS_ELASTIC_SEARCH: {
                        'STG': ImportValue('LeadMatching-STG-VPC'),
                        'PRD': ImportValue('LeadMatching-PRD-VPC'),
                    }
                },
                PEERING_DESTINATION_RANGE_CONFIG: {
                    PROSPECTS_ELASTIC_SEARCH: {
                        'STG': PROSPECTS_ELASTIC_SEARCH_CIDR,
                        'PRD': PROSPECTS_ELASTIC_SEARCH_CIDR,
                    }
                },
            }
        },
        ANALYTICS_PLATFORM: {
            SECOND_OCTET: VPC.get_second_octet(ANALYTICS_PLATFORM, ENVIRONMENT),
        },
        FORSIGHT_API: {
            SECOND_OCTET: VPC.get_second_octet(FORSIGHT_API, ENVIRONMENT),
        },
        NOTIFICATIONS_API: {
            SECOND_OCTET: VPC.get_second_octet(NOTIFICATIONS_API, ENVIRONMENT),
        },
        DATA_MOVER: {
            SECOND_OCTET: VPC.get_second_octet(DATA_MOVER, ENVIRONMENT),
        },
        MILO_API: {
            SECOND_OCTET: VPC.get_second_octet(MILO_API, ENVIRONMENT),
        },
        PROSPECTS_API: {
            SECOND_OCTET: VPC.get_second_octet(PROSPECTS_API, ENVIRONMENT),
            PUBLIC_SUBNETS_CONFIG: {
                'ProspectsDBA': '10.{0}.100.0/24'.format(
                    VPC.get_second_octet(PROSPECTS_API, ENVIRONMENT)),
                'ProspectsDBB': '10.{0}.101.0/24'.format(
                    VPC.get_second_octet(PROSPECTS_API, ENVIRONMENT)),
            }
        },
        OPPORTUNITY_FEEDER: {
            SECOND_OCTET: VPC.get_second_octet(OPPORTUNITY_FEEDER, ENVIRONMENT),
            PRIVATE_SUBNETS_CONFIG: {
                'OpportunityFeederDecisionModuleAgentA': '10.{0}.10.0/24'.format(
                    VPC.get_second_octet(OPPORTUNITY_FEEDER, ENVIRONMENT)),
                'OpportunityFeederDecisionModuleAgentB': '10.{0}.11.0/24'.format(
                    VPC.get_second_octet(OPPORTUNITY_FEEDER, ENVIRONMENT)),
                'OpportunityFeederUnfinishedMasterA': '10.{0}.12.0/24'.format(
                    VPC.get_second_octet(OPPORTUNITY_FEEDER, ENVIRONMENT)),
                'OpportunityFeederUnfinishedMasterB': '10.{0}.13.0/24'.format(
                    VPC.get_second_octet(OPPORTUNITY_FEEDER, ENVIRONMENT)),
                'OpportunityFeederUnfinishedAgentA': '10.{0}.14.0/24'.format(
                    VPC.get_second_octet(OPPORTUNITY_FEEDER, ENVIRONMENT)),
                'OpportunityFeederUnfinishedAgentB': '10.{0}.15.0/24'.format(
                    VPC.get_second_octet(OPPORTUNITY_FEEDER, ENVIRONMENT)),
            },
        },
    }

    APIVPC_PROJECTS = {
        FORWARDLINE_DB: {
            SECOND_OCTET: VPC.get_second_octet(PROJECT, ENVIRONMENT),
            PUBLIC_SUBNETS_CONFIG: {
                'ForwardlineDBA': '10.{0}.100.0/24'.format(
                    VPC.get_second_octet(PROJECT, ENVIRONMENT)),
                'ForwardlineDBB': '10.{0}.101.0/24'.format(
                    VPC.get_second_octet(PROJECT, ENVIRONMENT)),
            }
        },
        FORWARDLINE_CODEBUILD: {
            SECOND_OCTET: VPC.get_second_octet(PROJECT, ENVIRONMENT),
            PRIVATE_SUBNETS_CONFIG: {
                'ForwardlineCodeBuildA': '10.{0}.10.0/24'.format(
                    VPC.get_second_octet(PROJECT, ENVIRONMENT)),
                'ForwardlineCodeBuildB': '10.{0}.11.0/24'.format(
                    VPC.get_second_octet(PROJECT, ENVIRONMENT)),
            }
        }
    }

    CIDR = BASE_VPC_CIDR.format(VPC_SECOND_OCTET)
    PUBLIC_NAT_SUBNETS = {
        'NATA': '10.{0}.0.0/27'.format(VPC_SECOND_OCTET),
        'NATB': '10.{0}.0.32/27'.format(VPC_SECOND_OCTET),
    }
    PUBLIC_SUBNETS = {}
    PRIVATE_SUBNETS = {}
    NESTED_PUBLIC_SUBNETS = {}
    NESTED_PRIVATE_SUBNETS = {}

    PEERING_CONNECTIONS = {}

    for project, config in NESTED_PROJECTS.items():
        second_octet = config[SECOND_OCTET]
        NESTED_PROJECTS[project].update({'CIDR': BASE_VPC_CIDR.format(second_octet)})
        if PRIVATE_SUBNETS_CONFIG in config:
            NESTED_PRIVATE_SUBNETS.update(config[PRIVATE_SUBNETS_CONFIG])
        else:
            NESTED_PRIVATE_SUBNETS.update({'{0}A'.format(project): '10.{0}.10.0/24'.format(second_octet)})
            NESTED_PRIVATE_SUBNETS.update({'{0}B'.format(project): '10.{0}.11.0/24'.format(second_octet)})
        if PUBLIC_SUBNETS_CONFIG in config:
            NESTED_PUBLIC_SUBNETS.update(config[PUBLIC_SUBNETS_CONFIG])

    for project, config in PROJECTS.items():
        second_octet = config[SECOND_OCTET]
        PROJECTS[project].update({'CIDR': BASE_VPC_CIDR.format(second_octet)})
        if PRIVATE_SUBNETS_CONFIG in config:
            PRIVATE_SUBNETS.update(config[PRIVATE_SUBNETS_CONFIG])
        else:
            PRIVATE_SUBNETS.update({'{0}A'.format(project): '10.{0}.10.0/24'.format(second_octet)})
            PRIVATE_SUBNETS.update({'{0}B'.format(project): '10.{0}.11.0/24'.format(second_octet)})
        if PUBLIC_SUBNETS_CONFIG in config:
            PUBLIC_SUBNETS.update(config[PUBLIC_SUBNETS_CONFIG])

    for project, config in APIVPC_PROJECTS.items():
        second_octet = config[SECOND_OCTET]
        if PRIVATE_SUBNETS_CONFIG in config:
            PRIVATE_SUBNETS.update(config[PRIVATE_SUBNETS_CONFIG])
        if PUBLIC_SUBNETS_CONFIG in config:
            PUBLIC_SUBNETS.update(config[PUBLIC_SUBNETS_CONFIG])


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
                    peering_connection_name = '{0}-to-{1}-{2}'.format(self.PROJECT, vpc_name, self.ENVIRONMENT)
                    peering_connection = self.ec2_helper.create_peering_connection(
                        vpc=Ref(self.vpc),
                        peer_vpc=peering_config[self.PEERING_DESTINATION_VPC_CONFIG][vpc_name][self.ENVIRONMENT],
                        peer_name=peering_connection_name,
                        name_prefix=vpc_name
                    )
                    self.PEERING_CONNECTIONS.update({vpc_name: peering_connection})

                    """ Routes to Peering Connection for this VPC """
                    project_route_tables = [route_table for route_table in self.private_route_tables if project in route_table.title]
                    for route_table in project_route_tables:
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
    api_vpc.init_nested_template()
    print(api_vpc.t.to_json())
