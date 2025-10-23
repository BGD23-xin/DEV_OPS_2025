# VPC

官方定义是创建一个独立的网络环境，之后在这个环境上部署项目的资源。主要特点是`可控`，`安全`,`方便管理资源`
需要注意的是，VPC是区域性质的，即当前区域下的vpc，在其他区域下，无法显示。

它的组件分为两大类：
    -区域组件
    -跨区组件

## 区域组件

区域组件包含：
- VPC: vpc，一个区域由多个vpc，根据实际需求来创建
- Rubnet：子网，是在创建vpc时按照需求来创建，也能手动创建来划分区域，一般推荐在vpc内创建

下面4个组件是创建完vpc后会创建一个默认的，一般不需要再添加。
- Route table ： 路由表
- Internet gateway： 互联网网关
- DHCP option set ： VPC 会自动关联一个“默认 DHCP Option Set”，用于分配 DNS、域名等
- NAT gateways ： NAT网关，用于私有子网访问外网

下面需要手动添加
- security group ： 安全组,限制流量的进出, vpc创建时会有一个默认的，这个很基础，需要自行添加来创建安全组 
- Egress-only internet gateway : ipv6的出站网关设置
- Elastic IPs: 弹性IP,分配一个静态的ipv4 来给公有子网上的实例 被外部访问，不能分配给私有子网（私有子网没有连igw,所以没用）。
- Endpoints: 建立通道访问 private设置的资源，需要有prefix list


## 跨区组件
- Endpoint services：建立特殊通道来跨区访问 部署的`特定`资源，需要prefix list
- peering connections ：建立一个宽泛的通道来连接不同区域的vpc。可以用prefix list
- Managed prefix list：给访问资源一个静态的域名来让vpc内的资源访问，可跨区，本质是路由条目。所以一般添加到路由表内，作为一个目的转发。也可以作为出站目的地来限制访问来源。
