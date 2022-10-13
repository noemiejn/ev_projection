CELERY_BROKER_URL_DOCKER = "amqp://admin:mypass@rabbit:5672/"
CELERY_BROKER_URL_LOCAL = "amqp://localhost/"


CM_REGISTER_Q = "rpc_queue_CM_register"  # Do no change this value

CM_NAME = "CM - Electric vahicule density map"
RPC_CM_ALIVE = "rpc_queue_CM_ALIVE"  # Do no change this value
RPC_Q = "rpc_queue_CM_compute"  # Do no change this value
CM_ID = 1  # CM_ID is defined by the enegy research center of Martigny (CREM)
PORT_LOCAL = int("500" + str(CM_ID))
PORT_DOCKER = 80

# TODO ********************setup this URL depending on which version you are running***************************

CELERY_BROKER_URL = CELERY_BROKER_URL_DOCKER
PORT = PORT_DOCKER

# TODO ********************setup this URL depending on which version you are running***************************

TRANFER_PROTOCOLE = "http://"
INPUTS_CALCULATION_MODULE = [
    {
        "input_name": "Vehicles per habitant",
        "input_type": "input",
        "input_parameter_name": "vehicles_per_habitant",
        "input_value": 0.56,
        "input_priority": 0,
        "input_unit": "V./hab.",
        "input_min": 0,
        "input_max": 2,
        "cm_id": CM_ID,  # Do no change this value
    },
    {
        "input_name": "Vehicles rural-urban correction factor",
        "input_type": "input",
        "input_parameter_name": "vehicle_rural_urban_factor",
        "input_value": 20,
        "input_priority": 0.1,
        "input_unit": "%",
        "input_min": 0,
        "input_max": 90,
        "cm_id": CM_ID,  # Do no change this value
    },
    {
        "input_name": "Projection year",
        "input_type": "range",
        "input_parameter_name": "projection_year",
        "input_value": "2022",
        "input_priority": 0,
        "input_unit": "none",
        "input_min": 2022,
        "input_max": 2050,
        "cm_id": CM_ID,  # Do no change this value
    },
    {
        "input_name": "Mean battery capacity of the ev-fleat",
        "input_type": "range",
        "input_parameter_name": "battery_capacity",
        "input_value": "67",
        "input_priority": 0,
        "input_unit": "kWh",
        "input_min": 22,
        "input_max": 150,
        "cm_id": CM_ID,  # Do no change this value
    },
    {
        "input_name": "Daily traveled distance",
        "input_type": "range",
        "input_parameter_name": "daily_traveled_diatance",
        "input_value": "20",
        "input_priority": 0,
        "input_unit": "km",
        "input_min": 0,
        "input_max": 50,
        "cm_id": CM_ID,  # Do no change this value
    },
]


SIGNATURE = {
    "category": "Demand",
    "cm_name": CM_NAME,
    "wiki_url": "https://wiki.hotmaps.hevs.ch/en/CM-Scale-heat-and-cool-density-maps",
    "layers_needed": ["pop_tot_curr_density"],
    "type_layer_needed": [
        {"type": "population", "description": "Choose a population density layer."}
    ],
    "type_vectors_needed": [],  # ["pop_tot_density_2018"],  # Put here new vector layer of population
    "cm_url": "Do not add something",
    "cm_description": "This calculation module allows to scale the electric vehicule density layer up or down.",
    "cm_id": CM_ID,
    "inputs_calculation_module": INPUTS_CALCULATION_MODULE,
}
