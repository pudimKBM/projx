import requests
import json
import jsonref
from jsonschema import validate
import jsonschema
import traceback
import sys

try:
    json_str = {
        "quote": {
            "insurance_holder": {
                "$ref": "#/definitions/insurance_holder",
                "required": ["birth_date"],
            }
        },
        "contract": {
            "insurance_holder": {
                "$ref": "#/definitions/insurance_holder",
                "required": ["addresses", "name", "phones", "cpf", "email"],
                "properties": {
                    "phones": {
                        "type": "array",
                        "items": {
                            "$ref": "#/definitions/phone",
                            "required": ["number", "area_code"],
                        },
                    },
                    "addresses": {
                        "type": "array",
                        "items": {
                            "$ref": "#/definitions/address",
                            "required": [
                                "number",
                                "street",
                                "additional_details",
                                "zipcode",
                                "district",
                                "city",
                                "state",
                            ],
                        },
                    },
                },
            }
        },
        "definitions": {
            "phone": {
                "type": "object",
                "properties": {
                    "number": {"type": "string"},
                    "area_code": {"type": "string"},
                    "extension": {"type": "string"},
                },
            },
            "address": {
                "type": "object",
                "titles": {"pt-br": "Endereço"},
                "properties": {
                    "city": {"type": "string", "titles": {"pt-br": "Cidade"}},
                    "state": {"type": "string", "titles": {"pt-br": "Estado"}},
                    "number": {"type": "string", "titles": {"pt-br": "Número"}},
                    "street": {"type": "string", "titles": {"pt-br": "Logradouro"}},
                    "zipcode": {"type": "string", "titles": {"pt-br": "Cep"}},
                    "district": {"type": "string", "titles": {"pt-br": "Bairro"}},
                    "additional_details": {
                        "type": "string",
                        "titles": {"pt-br": "Complemento"},
                    },
                    "country": {"type": "string", "titles": {"pt-br": "País"}},
                },
            },
            "insurance_holder": {
                "type": "object",
                "titles": {"pt-br": "Segurado"},
                "properties": {
                    "cpf": {"type": "string", "titles": {"pt-br": "CPF"}},
                    "name": {"type": "string", "titles": {"pt-br": "Nome"}},
                    "email": {"type": "string"},
                    "addresses": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/address"},
                        "titles": {"pt-br": "Endereços"},
                    },
                    "birth_date": {
                        "type": "string",
                        "titles": {"pt-br": "Data de nascimento"},
                    },
                },
                "$ref": "#/definitions/person",
            },
            "relative": {
                "$ref": "#/definitions/person",
                "properties": {
                    "relationship": {
                        "type": "string",
                        "titles": {"pt-br": "Relação com o segurado"},
                    }
                },
            },
            "relatives": {
                "type": "array",
                "titles": {"pt-br": "Familiares"},
                "items": {"$ref": "#/definitions/relative"},
            },
            "pet": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "titles": {"pt-br": "Nome"}},
                    "species": {"type": "string", "titles": {"pt-br": "Espécie"}},
                    "breed": {"type": "string", "titles": {"pt-br": "Raça"}},
                    "size": {"type": "string", "titles": {"pt-br": "Tamanho"}},
                    "gender": {"type": "string", "titles": {"pt-br": "Gênero"}},
                    "age": {"type": "integer", "titles": {"pt-br": "Idade"}},
                    "birth_date": {
                        "type": "string",
                        "titles": {"pt-br": "Data de nascimento"},
                    },
                    "preexisting_condition": {
                        "type": "string",
                        "titles": {"pt-br": "Condição pré-existente"},
                    },
                    "vaccined": {"type": "string", "titles": {"pt-br": "Vacinado"}},
                    "condition_description": {
                        "type": "string",
                        "titles": {"pt-br": "Descrição da condição"},
                    },
                },
            },
            "person": {
                "type": "object",
                "titles": {"pt-br": "Pessoa"},
                "properties": {
                    "cpf": {"type": "string", "titles": {"pt-br": "CPF"}},
                    "rg": {
                        "type": "object",
                        "titles": {"pt-br": "RG"},
                        "properties": {
                            "number": {"type": "string", "titles": {"pt-br": "Número"}},
                            "issuing_agency": {
                                "type": "string",
                                "titles": {"pt-br": "Orgão emissor"},
                            },
                            "issue_date": {
                                "type": "string",
                                "titles": {"pt-br": "Data de emissão"},
                            },
                        },
                    },
                    "name": {"type": "string", "titles": {"pt-br": "Nome"}},
                    "birth_date": {
                        "type": "string",
                        "titles": {"pt-br": "Data de nascimento"},
                    },
                    "gender": {"type": "string", "titles": {"pt-br": "Gênero"}},
                    "email": {"type": "string", "titles": {"pt-br": "Email"}},
                    "addresses": {
                        "type": "array",
                        "titles": {"pt-br": "Endereços"},
                        "items": {"$ref": "#/definitions/address"},
                    },
                    "phones": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/phone"},
                    },
                    "profession": {"type": "string", "titles": {"pt-br": "Profissão"}},
                    "marital_status": {
                        "type": "string",
                        "titles": {"pt-br": "Estado civil"},
                    },
                    "politically_exposed": {
                        "titles": {"pt-br": "Pessoa politicamente exposta"},
                        "type": "boolean",
                    },
                },
            },
            "risk_people": {
                "type": "array",
                "items": {"$ref": "#/definitions/risk_person"},
            },
            "risk_person": {"$ref": "#/definitions/person"},
            "risk_address": {
                "$ref": "#/definitions/address",
                "type": "object",
                "properties": {
                    "occupation_type": {
                        "type": "string",
                        "titles": {"pt-br": "Tipo de ocupação"},
                    },
                    "construction_type": {
                        "type": "string",
                        "titles": {"pt-br": "Tipo de construção"},
                    },
                    "residence_type": {
                        "type": "string",
                        "titles": {"pt-br": "Tipo de residência"},
                    },
                    "occupation": {"type": "string", "titles": {"pt-br": "Ocupação"}},
                    "location": {"type": "string", "titles": {"pt-br": "Localização"}},
                },
            },
            "risk_car": {
                "type": "object",
                "titles": {"pt-br": "Carro segurado"},
                "properties": {
                    "make": {"type": "string", "titles": {"pt-br": "Marca"}},
                    "model": {"type": "string", "titles": {"pt-br": "Modelo"}},
                    "license_plate": {"type": "string", "titles": {"pt-br": "Placa"}},
                    "vin": {"type": "string", "titles": {"pt-br": "Chassi"}},
                    "renavam": {"type": "string", "titles": {"pt-br": "Renavam"}},
                    "manufacture_year": {
                        "type": "string",
                        "titles": {"pt-br": "Ano de fabricação"},
                    },
                    "model_year": {
                        "type": "string",
                        "titles": {"pt-br": "Ano do modelo"},
                    },
                    "cargo_type": {
                        "type": "string",
                        "titles": {"pt-br": "Tipo de carga"},
                    },
                    "fuel_type": {
                        "type": "string",
                        "titles": {"pt-br": "Tipo de combustível"},
                    },
                    "color": {"type": "string", "titles": {"pt-br": "Cor"}},
                    "fipe_code": {"type": "string", "titles": {"pt-br": "Código fipe"}},
                },
            },
            "payment": {
                "type": "object",
                "titles": {"pt-br": "Pagamento"},
                "properties": {
                    "id_opcao_pagamento": {
                        "titles": {"pt-br": "Opção de pagamento escolhida"},
                        "type": "integer",
                    },
                    "billing_address": {
                        "$ref": "#/definitions/address",
                        "titles": {"pt-br": "Endereço de cobrança"},
                    },
                },
            },
        },
    }

    data_valid = {
  "quote": {
    "insurance_holder": {
      "birth_date": "non aliquip Lorem enim sed"
    }
  },
  "contract": {
    "insurance_holder": {
      "addresses": [
        {
          "number": "dolore veniam l",
          "street": "velit ad",
          "additional_details": "qui consectetur velit fugiat dolore",
          "zipcode": "dolor esse Lorem elit",
          "district": "Excepteur magna",
          "city": "in est minim laboris labore",
          "state": "aute sit laboris"
        }
      ],
      "phones": [
        {
          "number": "officia",
          "area_code": "voluptate in L"
        },
        {
          "number": "volupt",
          "area_code": "eiusmod irure pariatur"
        },
        {
          "number": "culpa mollit aute anim",
          "area_code": "ex"
        },
        {
          "number": "ex culpa",
          "area_code": "Lore"
        }
      ]
    }
  },
  "definitions": {
    "phone": {
      "type": "object",
      "properties": {
        "number": {
          "type": "string"
        },
        "area_code": {
          "type": "string"
        },
        "extension": {
          "type": "string"
        }
      }
    },
    "address": {
      "type": "object",
      "titles": {
        "pt-br": "Endereço"
      },
      "properties": {
        "city": {
          "type": "string",
          "titles": {
            "pt-br": "Cidade"
          }
        },
        "state": {
          "type": "string",
          "titles": {
            "pt-br": "Estado"
          }
        },
        "number": {
          "type": "string",
          "titles": {
            "pt-br": "Número"
          }
        },
        "street": {
          "type": "string",
          "titles": {
            "pt-br": "Logradouro"
          }
        },
        "zipcode": {
          "type": "string",
          "titles": {
            "pt-br": "Cep"
          }
        },
        "district": {
          "type": "string",
          "titles": {
            "pt-br": "Bairro"
          }
        },
        "additional_details": {
          "type": "string",
          "titles": {
            "pt-br": "Complemento"
          }
        },
        "country": {
          "type": "string",
          "titles": {
            "pt-br": "País"
          }
        }
      }
    },
    "insurance_holder": {
      "type": "object",
      "titles": {
        "pt-br": "Segurado"
      },
      "properties": {
        "cpf": {
          "type": "string",
          "titles": {
            "pt-br": "CPF"
          }
        },
        "name": {
          "type": "string",
          "titles": {
            "pt-br": "Nome"
          }
        },
        "email": {
          "type": "string"
        },
        "addresses": {
          "type": "array",
          "items": {
            "type": "object",
            "titles": {
              "pt-br": "Endereço"
            },
            "properties": {
              "city": {
                "type": "string",
                "titles": {
                  "pt-br": "Cidade"
                }
              },
              "state": {
                "type": "string",
                "titles": {
                  "pt-br": "Estado"
                }
              },
              "number": {
                "type": "string",
                "titles": {
                  "pt-br": "Número"
                }
              },
              "street": {
                "type": "string",
                "titles": {
                  "pt-br": "Logradouro"
                }
              },
              "zipcode": {
                "type": "string",
                "titles": {
                  "pt-br": "Cep"
                }
              },
              "district": {
                "type": "string",
                "titles": {
                  "pt-br": "Bairro"
                }
              },
              "additional_details": {
                "type": "string",
                "titles": {
                  "pt-br": "Complemento"
                }
              },
              "country": {
                "type": "string",
                "titles": {
                  "pt-br": "País"
                }
              }
            }
          },
          "titles": {
            "pt-br": "Endereços"
          }
        },
        "birth_date": {
          "type": "string",
          "titles": {
            "pt-br": "Data de nascimento"
          }
        }
      }
    },
    "relative": {
      "properties": {
        "relationship": {
          "type": "string",
          "titles": {
            "pt-br": "Relação com o segurado"
          }
        }
      },
      "type": "object",
      "titles": {
        "pt-br": "Pessoa"
      }
    },
    "relatives": {
      "type": "array",
      "titles": {
        "pt-br": "Familiares"
      },
      "items": {
        "properties": {
          "relationship": {
            "type": "string",
            "titles": {
              "pt-br": "Relação com o segurado"
            }
          }
        },
        "type": "object",
        "titles": {
          "pt-br": "Pessoa"
        }
      }
    },
    "pet": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "titles": {
            "pt-br": "Nome"
          }
        },
        "species": {
          "type": "string",
          "titles": {
            "pt-br": "Espécie"
          }
        },
        "breed": {
          "type": "string",
          "titles": {
            "pt-br": "Raça"
          }
        },
        "size": {
          "type": "string",
          "titles": {
            "pt-br": "Tamanho"
          }
        },
        "gender": {
          "type": "string",
          "titles": {
            "pt-br": "Gênero"
          }
        },
        "age": {
          "type": "integer",
          "titles": {
            "pt-br": "Idade"
          }
        },
        "birth_date": {
          "type": "string",
          "titles": {
            "pt-br": "Data de nascimento"
          }
        },
        "preexisting_condition": {
          "type": "string",
          "titles": {
            "pt-br": "Condição pré-existente"
          }
        },
        "vaccined": {
          "type": "string",
          "titles": {
            "pt-br": "Vacinado"
          }
        },
        "condition_description": {
          "type": "string",
          "titles": {
            "pt-br": "Descrição da condição"
          }
        }
      }
    },
    "person": {
      "type": "object",
      "titles": {
        "pt-br": "Pessoa"
      },
      "properties": {
        "cpf": {
          "type": "string",
          "titles": {
            "pt-br": "CPF"
          }
        },
        "rg": {
          "type": "object",
          "titles": {
            "pt-br": "RG"
          },
          "properties": {
            "number": {
              "type": "string",
              "titles": {
                "pt-br": "Número"
              }
            },
            "issuing_agency": {
              "type": "string",
              "titles": {
                "pt-br": "Orgão emissor"
              }
            },
            "issue_date": {
              "type": "string",
              "titles": {
                "pt-br": "Data de emissão"
              }
            }
          }
        },
        "name": {
          "type": "string",
          "titles": {
            "pt-br": "Nome"
          }
        },
        "birth_date": {
          "type": "string",
          "titles": {
            "pt-br": "Data de nascimento"
          }
        },
        "gender": {
          "type": "string",
          "titles": {
            "pt-br": "Gênero"
          }
        },
        "email": {
          "type": "string",
          "titles": {
            "pt-br": "Email"
          }
        },
        "addresses": {
          "type": "array",
          "titles": {
            "pt-br": "Endereços"
          },
          "items": {
            "type": "object",
            "titles": {
              "pt-br": "Endereço"
            },
            "properties": {
              "city": {
                "type": "string",
                "titles": {
                  "pt-br": "Cidade"
                }
              },
              "state": {
                "type": "string",
                "titles": {
                  "pt-br": "Estado"
                }
              },
              "number": {
                "type": "string",
                "titles": {
                  "pt-br": "Número"
                }
              },
              "street": {
                "type": "string",
                "titles": {
                  "pt-br": "Logradouro"
                }
              },
              "zipcode": {
                "type": "string",
                "titles": {
                  "pt-br": "Cep"
                }
              },
              "district": {
                "type": "string",
                "titles": {
                  "pt-br": "Bairro"
                }
              },
              "additional_details": {
                "type": "string",
                "titles": {
                  "pt-br": "Complemento"
                }
              },
              "country": {
                "type": "string",
                "titles": {
                  "pt-br": "País"
                }
              }
            }
          }
        },
        "phones": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "number": {
                "type": "string"
              },
              "area_code": {
                "type": "string"
              },
              "extension": {
                "type": "string"
              }
            }
          }
        },
        "profession": {
          "type": "string",
          "titles": {
            "pt-br": "Profissão"
          }
        },
        "marital_status": {
          "type": "string",
          "titles": {
            "pt-br": "Estado civil"
          }
        },
        "politically_exposed": {
          "titles": {
            "pt-br": "Pessoa politicamente exposta"
          },
          "type": "boolean"
        }
      }
    },
    "risk_people": {
      "type": "array",
      "items": {
        "type": "object",
        "titles": {
          "pt-br": "Pessoa"
        },
        "properties": {
          "cpf": {
            "type": "string",
            "titles": {
              "pt-br": "CPF"
            }
          },
          "rg": {
            "type": "object",
            "titles": {
              "pt-br": "RG"
            },
            "properties": {
              "number": {
                "type": "string",
                "titles": {
                  "pt-br": "Número"
                }
              },
              "issuing_agency": {
                "type": "string",
                "titles": {
                  "pt-br": "Orgão emissor"
                }
              },
              "issue_date": {
                "type": "string",
                "titles": {
                  "pt-br": "Data de emissão"
                }
              }
            }
          },
          "name": {
            "type": "string",
            "titles": {
              "pt-br": "Nome"
            }
          },
          "birth_date": {
            "type": "string",
            "titles": {
              "pt-br": "Data de nascimento"
            }
          },
          "gender": {
            "type": "string",
            "titles": {
              "pt-br": "Gênero"
            }
          },
          "email": {
            "type": "string",
            "titles": {
              "pt-br": "Email"
            }
          },
          "addresses": {
            "type": "array",
            "titles": {
              "pt-br": "Endereços"
            },
            "items": {
              "type": "object",
              "titles": {
                "pt-br": "Endereço"
              },
              "properties": {
                "city": {
                  "type": "string",
                  "titles": {
                    "pt-br": "Cidade"
                  }
                },
                "state": {
                  "type": "string",
                  "titles": {
                    "pt-br": "Estado"
                  }
                },
                "number": {
                  "type": "string",
                  "titles": {
                    "pt-br": "Número"
                  }
                },
                "street": {
                  "type": "string",
                  "titles": {
                    "pt-br": "Logradouro"
                  }
                },
                "zipcode": {
                  "type": "string",
                  "titles": {
                    "pt-br": "Cep"
                  }
                },
                "district": {
                  "type": "string",
                  "titles": {
                    "pt-br": "Bairro"
                  }
                },
                "additional_details": {
                  "type": "string",
                  "titles": {
                    "pt-br": "Complemento"
                  }
                },
                "country": {
                  "type": "string",
                  "titles": {
                    "pt-br": "País"
                  }
                }
              }
            }
          },
          "phones": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "number": {
                  "type": "string"
                },
                "area_code": {
                  "type": "string"
                },
                "extension": {
                  "type": "string"
                }
              }
            }
          },
          "profession": {
            "type": "string",
            "titles": {
              "pt-br": "Profissão"
            }
          },
          "marital_status": {
            "type": "string",
            "titles": {
              "pt-br": "Estado civil"
            }
          },
          "politically_exposed": {
            "titles": {
              "pt-br": "Pessoa politicamente exposta"
            },
            "type": "boolean"
          }
        }
      }
    },
    "risk_person": {
      "type": "object",
      "titles": {
        "pt-br": "Pessoa"
      },
      "properties": {
        "cpf": {
          "type": "string",
          "titles": {
            "pt-br": "CPF"
          }
        },
        "rg": {
          "type": "object",
          "titles": {
            "pt-br": "RG"
          },
          "properties": {
            "number": {
              "type": "string",
              "titles": {
                "pt-br": "Número"
              }
            },
            "issuing_agency": {
              "type": "string",
              "titles": {
                "pt-br": "Orgão emissor"
              }
            },
            "issue_date": {
              "type": "string",
              "titles": {
                "pt-br": "Data de emissão"
              }
            }
          }
        },
        "name": {
          "type": "string",
          "titles": {
            "pt-br": "Nome"
          }
        },
        "birth_date": {
          "type": "string",
          "titles": {
            "pt-br": "Data de nascimento"
          }
        },
        "gender": {
          "type": "string",
          "titles": {
            "pt-br": "Gênero"
          }
        },
        "email": {
          "type": "string",
          "titles": {
            "pt-br": "Email"
          }
        },
        "addresses": {
          "type": "array",
          "titles": {
            "pt-br": "Endereços"
          },
          "items": {
            "type": "object",
            "titles": {
              "pt-br": "Endereço"
            },
            "properties": {
              "city": {
                "type": "string",
                "titles": {
                  "pt-br": "Cidade"
                }
              },
              "state": {
                "type": "string",
                "titles": {
                  "pt-br": "Estado"
                }
              },
              "number": {
                "type": "string",
                "titles": {
                  "pt-br": "Número"
                }
              },
              "street": {
                "type": "string",
                "titles": {
                  "pt-br": "Logradouro"
                }
              },
              "zipcode": {
                "type": "string",
                "titles": {
                  "pt-br": "Cep"
                }
              },
              "district": {
                "type": "string",
                "titles": {
                  "pt-br": "Bairro"
                }
              },
              "additional_details": {
                "type": "string",
                "titles": {
                  "pt-br": "Complemento"
                }
              },
              "country": {
                "type": "string",
                "titles": {
                  "pt-br": "País"
                }
              }
            }
          }
        },
        "phones": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "number": {
                "type": "string"
              },
              "area_code": {
                "type": "string"
              },
              "extension": {
                "type": "string"
              }
            }
          }
        },
        "profession": {
          "type": "string",
          "titles": {
            "pt-br": "Profissão"
          }
        },
        "marital_status": {
          "type": "string",
          "titles": {
            "pt-br": "Estado civil"
          }
        },
        "politically_exposed": {
          "titles": {
            "pt-br": "Pessoa politicamente exposta"
          },
          "type": "boolean"
        }
      }
    },
    "risk_address": {
      "type": "object",
      "properties": {
        "occupation_type": {
          "type": "string",
          "titles": {
            "pt-br": "Tipo de ocupação"
          }
        },
        "construction_type": {
          "type": "string",
          "titles": {
            "pt-br": "Tipo de construção"
          }
        },
        "residence_type": {
          "type": "string",
          "titles": {
            "pt-br": "Tipo de residência"
          }
        },
        "occupation": {
          "type": "string",
          "titles": {
            "pt-br": "Ocupação"
          }
        },
        "location": {
          "type": "string",
          "titles": {
            "pt-br": "Localização"
          }
        }
      },
      "titles": {
        "pt-br": "Endereço"
      }
    },
    "risk_car": {
      "type": "object",
      "titles": {
        "pt-br": "Carro segurado"
      },
      "properties": {
        "make": {
          "type": "string",
          "titles": {
            "pt-br": "Marca"
          }
        },
        "model": {
          "type": "string",
          "titles": {
            "pt-br": "Modelo"
          }
        },
        "license_plate": {
          "type": "string",
          "titles": {
            "pt-br": "Placa"
          }
        },
        "vin": {
          "type": "string",
          "titles": {
            "pt-br": "Chassi"
          }
        },
        "renavam": {
          "type": "string",
          "titles": {
            "pt-br": "Renavam"
          }
        },
        "manufacture_year": {
          "type": "string",
          "titles": {
            "pt-br": "Ano de fabricação"
          }
        },
        "model_year": {
          "type": "string",
          "titles": {
            "pt-br": "Ano do modelo"
          }
        },
        "cargo_type": {
          "type": "string",
          "titles": {
            "pt-br": "Tipo de carga"
          }
        },
        "fuel_type": {
          "type": "string",
          "titles": {
            "pt-br": "Tipo de combustível"
          }
        },
        "color": {
          "type": "string",
          "titles": {
            "pt-br": "Cor"
          }
        },
        "fipe_code": {
          "type": "string",
          "titles": {
            "pt-br": "Código fipe"
          }
        }
      }
    },
    "payment": {
      "type": "object",
      "titles": {
        "pt-br": "Pagamento"
      },
      "properties": {
        "id_opcao_pagamento": {
          "titles": {
            "pt-br": "Opção de pagamento escolhida"
          },
          "type": "integer"
        },
        "billing_address": {
          "titles": {
            "pt-br": "Endereço de cobrança"
          },
          "type": "object",
          "properties": {
            "city": {
              "type": "string",
              "titles": {
                "pt-br": "Cidade"
              }
            },
            "state": {
              "type": "string",
              "titles": {
                "pt-br": "Estado"
              }
            },
            "number": {
              "type": "string",
              "titles": {
                "pt-br": "Número"
              }
            },
            "street": {
              "type": "string",
              "titles": {
                "pt-br": "Logradouro"
              }
            },
            "zipcode": {
              "type": "string",
              "titles": {
                "pt-br": "Cep"
              }
            },
            "district": {
              "type": "string",
              "titles": {
                "pt-br": "Bairro"
              }
            },
            "additional_details": {
              "type": "string",
              "titles": {
                "pt-br": "Complemento"
              }
            },
            "country": {
              "type": "string",
              "titles": {
                "pt-br": "País"
              }
            }
          }
        }
      }
    }
  }
}
    
    datax = json.dumps(json_str)
    data = json.loads(datax)
    valid_data = json.dumps(data_valid)
    valid_datax = json.loads(valid_data)

    
    try:
        validate(instance=valid_datax, schema=data)
    except jsonschema.ValidationError as e:
        print("error : cabo , CABOLOSO")
    else:
        print("# If no exception is raised by validate(), the instance is valid.")



except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    traceback.print_tb(e.__traceback__)
