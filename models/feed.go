package models

import "github.com/uadmin/uadmin"

type Feeds struct {
	uadmin.Model
	Url string `uadmin:"required;search"` 
	Publisher Publisher
	PublisherID uint
	Category Category
	CategoryID uint
	Language uadmin.Language
	LanguageID uint
	Duration uint
	Flashcard uint
	Age_group uint
}


// FolderUser function that returns string value
func (f *Feeds) String() string {

    // Gives access to the fields in another model
    uadmin.Preload(f)

    // Returns the full name from the User model
    return f.Category.Name
}
