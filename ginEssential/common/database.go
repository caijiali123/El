package common

import (
	"ginEssential/model"
	"github.com/jinzhu/gorm"
)

var DB *gorm.DB

// 连接database
func InitDB() *gorm.DB {

	args := "data_analysis:F8taJfkU%FE@tcp(10.132.166.89:4000)/data_analysis?charset=utf8mb4&parseTime=True&loc=Local"
	db, err := gorm.Open("mysql", args)
	if err != nil {
		panic("failed to connect database,err:" + err.Error())
	}

	db.AutoMigrate(&model.User{})

	DB = db
	return db
}

func GetDB() *gorm.DB {
	return DB
}
