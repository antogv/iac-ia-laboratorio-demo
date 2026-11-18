output "resumen" {
  description = "Datos previstos tras una aplicación local"
  value = {
    portal = module.portal.resumen
    ayuda  = module.ayuda.resumen
  }
}
