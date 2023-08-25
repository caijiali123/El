package main

import (
	"ginEssential/controller"
	"ginEssential/middleware"
	"github.com/gin-gonic/gin"
)

func CollectRoute(r *gin.Engine) *gin.Engine {
	r.POST("/api/auth/register", controller.Register) //注册

	r.POST("/api/auth/login", controller.Login) //登陆

	r.GET("api/auth/info", middleware.AuthMiddleware(), controller.Info)

	return r
}
