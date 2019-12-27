package models

import "github.com/uadmin/uadmin"

type Publisher struct {
	uadmin.Model
	Name string `uadmin:"required;search;multilingual"` 
	Icon string `uadmin:"image"`
}

