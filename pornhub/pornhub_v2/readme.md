相关资料
https://splash.readthedocs.io/en/latest/scripting-ref.html#splash-evaljs
https://www.runoob.com/lua/lua-tutorial.html

1.docker部署splash
    1.1 安装DockerToolbox
        参考 https://docs.docker.com/toolbox/toolbox_install_windows/
        首先控制面板关闭 Hyper-V 、container 并且 cmd执行   bcdedit /set hypervisorlaunchtype off
        完成之后有一个Docker Quickstart Terminal、Kitematic (Alpha)、Oracle VM VirtualBox，正常来说点击Docker Quickstart Terminal即可打开虚拟机和使用docker-machine -h
        连接虚拟机shell     docker-machine ssh default
        默认用户名：docker 密码：tcuser
        切换到root用户，docker用户下执行 sudo -i
        配置国内镜像源
        vi /etc/docker/daemon.json
        {
            "registry-mirrors": ["https://registry.docker-cn.com","http://hub-mirror.c.163.com"]
        }
    1.2 安装portainer管理containers
        docker pull portainer/portainer
        docker volume create portainer_data
        docker run -d -p 9000:9000 -p 8000:8000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
    1.3 安装splash
        docker pull scrapinghub/splash
        docker run -d -it -p 8050:8050 scrapinghub/splash --max-timeout 3600
2.安装scrapy-splash
    pip install scrapy-splash
3.配置SPLASH的URL和代理
4.执行爬虫