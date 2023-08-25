package main

import (
	"ginEssential/common"
	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql"
)

// 连接数据库

func main() {
	db := common.InitDB()
	defer db.Close() //延迟关闭

	r := gin.Default()
	r = CollectRoute(r)

	panic(r.Run())
}
