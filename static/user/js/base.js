// /**
//  * Created by root on 17-6-10.
//  */
$(document).ready(function () {
//     // 点开或者关闭主菜单时改变菜单右边"箭头"
//     $(".menu").click(function () {
//             /*切换折叠指示图标*/
//             if ($(this).children("span:last").attr("class") == "glyphicon glyphicon-menu-left") {
//                 $(this).children("span:last").attr("class", "glyphicon glyphicon-menu-down");
//             } else {
//                 $(this).children("span:last").attr("class", "glyphicon glyphicon-menu-left");
//             }
//         }
//     );
//
//     // 打开某主菜单后折叠其他主菜单
//     $('.submenu').on('shown.bs.collapse', function () {
//         currentId = $(this).attr('id');
//
//         $(".submenu").each(function () {
//             Id = $(this).attr('id');
//             if (Id != currentId) {
//                 // $(this).attr("class", "submenu panel-collapse collapse");
//                 $(this).collapse('hide');
//                 // 其它菜单折叠后修改"箭头"为向左
//                 $(this).prev().children("span").last().attr("class", "glyphicon glyphicon-menu-left");
//             }
//         });
//     });
//
//     // // 鼠标移动到菜单上方时打开二级菜单
//     // $(".menu").hover(
//     //     function () {
//     //         $(this).next().collapse('show');
//     //         $(this).children("span:last").attr("class", "glyphicon glyphicon-menu-down");
//     //     },
//     //     function () {
//     //     }
//     // );
//
//     $('.submenu').on(("click", "[data-stopPropagation]", function (event) {
//         event.stopPropagation();
//     });
    $(".submenu a[data-stopPropagation]").click(function (event) {
        event.stopPropagation();
        $(this).addClass('active');
    });

});