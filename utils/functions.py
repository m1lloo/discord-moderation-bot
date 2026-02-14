import os

def parse_role_ids(env_var):
    return [int(id.strip()) for id in os.getenv(env_var, "").split(",") if id.strip()]