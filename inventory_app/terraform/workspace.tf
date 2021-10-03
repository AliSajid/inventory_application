terraform {
  backend "remote" {
    organization = "Imamiland"

    workspaces {
      name = "InventoryApp"
    }
  }
}
