package controller

import (
	"ginEssential/common"
	"ginEssential/dto"
	"ginEssential/model"
	"ginEssential/response"
	"ginEssential/util"
	"github.com/gin-gonic/gin"
	"github.com/jinzhu/gorm"
	"golang.org/x/crypto/bcrypt"
	"log"
	"net/http"
)

func Register(ctx *gin.Context) {
	DB := common.GetDB()
	// 获取参数：前端传三个参数到后端：名称、手机号、密码
	name := ctx.PostForm("name")
	telephone := ctx.PostForm("telephone")
	password := ctx.PostForm("password")
	// 数据验证

	if len(telephone) != 11 {
		response.Response(ctx, http.StatusUnprocessableEntity, 422, nil, "手机号必须为11位")
		return
	}

	if len(password) != 6 {
		response.Response(ctx, http.StatusUnprocessableEntity, 422, nil, "密码不少于6位")
		return
	}
	//判断名称有没有传，如果没有则随机给一个10位字符串
	if len(name) == 0 {
		name = util.RandomString(10)
	}

	log.Println(name, telephone, password)

	// 判断用户是否存在 不存在则返回一个http的错误，如果存在则创建用户
	if isTelephoneExist(DB, telephone) {
		response.Response(ctx, http.StatusUnprocessableEntity, 422, nil, "用户已经存在")
		return
	}

	// 创建用户：写入database里面
	hasePassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)

	if err != nil {
		response.Response(ctx, http.StatusUnprocessableEntity, 500, nil, "加密错误")
		return
	}

	newUser := model.User{
		Name:      name,
		Telephone: telephone,
		Password:  string(hasePassword),
	}
	DB.Create(&newUser)

	// 返回结果
	response.Success(ctx, nil, "注册成功")

}

func Login(ctx *gin.Context) {
	DB := common.GetDB()
	//获取参数
	telephone := ctx.PostForm("telephone")
	password := ctx.PostForm("password")

	//数据验证
	if len(telephone) != 11 {
		ctx.JSON(http.StatusUnprocessableEntity, map[string]interface{}{"code": 422, "msg": "手机号必须为11位"})
		return
	}

	if len(password) != 6 {
		ctx.JSON(http.StatusUnprocessableEntity, map[string]interface{}{"code": 422, "msg": "密码不少于6位"})
		return
	}

	//判断手机号是否存在
	var user model.User
	DB.Where("telephone = ?", telephone).First(&user)

	if user.ID == 0 {
		ctx.JSON(http.StatusUnprocessableEntity, map[string]interface{}{"code": 422, "msg": "用户不存在"})
		return
	}

	//判断密码是否正确 正确：发放token给前端
	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password)); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"code": 400, "msg": "密码错误"})
		return
	}

	//发送token
	token, err := common.ReleaseToken(user)

	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"code": 500, "msg": "系统异常"})
		log.Printf("token generate error:%v", err)
		return
	}

	//返回结果
	response.Success(ctx, gin.H{"token": token}, "登陆成功")
}

func Info(ctx *gin.Context) {
	user, _ := ctx.Get("user")

	ctx.JSON(http.StatusOK, gin.H{"code": 200, "data": gin.H{"user": dto.ToUserDto(user.(model.User))}})
}

// 判断输入的手机是否在数据库中存在
// gorm对每一个记录的数据都会返回一个唯一ID 方便调用
func isTelephoneExist(db *gorm.DB, telephone string) bool {
	var user model.User
	db.Where("telephone = ?", telephone).First(&user)
	if user.ID != 0 {
		return true
	}
	return false
}
