import json
import sys


EXPECTED_ADDRESSES = {
    "module.portal.terraform_data.ficha",
    "module.ayuda.terraform_data.ficha",
}
ALLOWED_ENVIRONMENTS = {"desarrollo", "pruebas", "integracion"}


def reject(reason):
    print(f"POLÍTICA RECHAZADA: {reason}")
    return 1


def is_marked(metadata, path):
    current = metadata
    for part in path:
        if current is True:
            return True
        if not isinstance(current, dict):
            return False
        current = current.get(part)
    return current is True


def reject_nonstandard_constant(constant):
    raise ValueError(f"{constant} no es una constante JSON válida.")


def main():
    try:
        plan = json.load(sys.stdin, parse_constant=reject_nonstandard_constant)
    except json.JSONDecodeError as error:
        return reject(f"JSON no válido: {error.msg}.")
    except UnicodeDecodeError:
        return reject("la entrada no contiene texto UTF-8 válido.")
    except ValueError as error:
        return reject(f"JSON no válido: {error}.")

    if not isinstance(plan, dict) or "resource_changes" not in plan:
        return reject("el plan debe ser un objeto JSON con resource_changes.")

    changes = plan["resource_changes"]
    if not isinstance(changes, list):
        return reject("resource_changes debe ser una lista.")
    if len(changes) != 2:
        return reject("resource_changes debe contener exactamente dos cambios.")

    addresses = [item.get("address") for item in changes if isinstance(item, dict)]
    if (
        len(addresses) != 2
        or any(not isinstance(address, str) for address in addresses)
        or set(addresses) != EXPECTED_ADDRESSES
    ):
        return reject(
            "las direcciones deben ser exactamente "
            "module.portal.terraform_data.ficha y "
            "module.ayuda.terraform_data.ficha."
        )

    values_by_address = {}
    for resource_change in changes:
        address = resource_change["address"]
        if resource_change.get("mode") != "managed":
            return reject(f"{address} debe ser un recurso managed.")
        if resource_change.get("type") != "terraform_data":
            return reject(f"{address} debe ser de tipo terraform_data.")

        change = resource_change.get("change")
        if not isinstance(change, dict):
            return reject(f"{address} no contiene un objeto change válido.")
        if change.get("actions") != ["create"]:
            return reject(f"{address} debe tener como única acción [\"create\"].")

        after = change.get("after")
        if not isinstance(after, dict):
            return reject(f"{address} no contiene un objeto change.after válido.")
        inputs = after.get("input")
        if not isinstance(inputs, dict):
            return reject(f"{address} debe tener un objeto change.after.input.")

        for field in ("nombre", "entorno"):
            if field not in inputs:
                return reject(f"{address}: falta el valor {field} en input.")
            path = ("input", field)
            if is_marked(change.get("after_unknown", {}), path):
                return reject(f"{address}: el valor {field} es desconocido.")
            if is_marked(change.get("after_sensitive", {}), path):
                return reject(f"{address}: el valor {field} está marcado como sensible.")
            if not isinstance(inputs[field], str) or not inputs[field]:
                return reject(f"{address}: el valor {field} debe ser un texto no vacío.")
            values_by_address.setdefault(address, {})[field] = inputs[field]

    portal_name = values_by_address["module.portal.terraform_data.ficha"]["nombre"]
    ayuda_name = values_by_address["module.ayuda.terraform_data.ficha"]["nombre"]
    if not portal_name.startswith("portal-"):
        return reject("el nombre de portal debe comenzar por \"portal-\".")
    if ayuda_name != "portal-ayuda":
        return reject("el nombre de ayuda debe ser exactamente \"portal-ayuda\".")

    portal_environment = values_by_address["module.portal.terraform_data.ficha"]["entorno"]
    ayuda_environment = values_by_address["module.ayuda.terraform_data.ficha"]["entorno"]
    if portal_environment != ayuda_environment:
        return reject("los entornos de portal y ayuda deben ser iguales.")
    if portal_environment not in ALLOWED_ENVIRONMENTS:
        return reject("el entorno debe ser desarrollo, pruebas o integracion.")

    print(
        "POLÍTICA APROBADA: dos fichas ficticias, mismo entorno y sin operaciones reales"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
