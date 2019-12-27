package main

import (
	"github.com/uadmin/uadmin"
	"github.com/padmin/models"
)




func main() {
	
	uadmin.Database = &uadmin.DBSettings{
        Type:      "mysql",
        Name:      "padmin",
        User:      "root",
        Password:  "root",
        Host:      "127.0.0.1",
        Port:      3306,
    }
	
	
	uadmin.Register(
		models.Publisher{},
		models.Category{},
		models.Feeds{},
	)

	uadmin.StartServer()
}
