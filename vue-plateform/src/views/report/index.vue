<template>
<div>
<div class="heading1">
<div class='heading'>
    <el-button size="mini" type="primary" icon="el-icon-arrow-left" @click="back">上一页</el-button>
    <h1>  {{reportList.report_name}}测试报告</h1>
    <p class='attribute'><strong>Status:</strong>Count:{{reportList.case_num}} &nbsp; Pass:{{reportList.pass_num}}&nbsp;
        Fail:{{reportList.fail_num}} &nbsp; Error:{{reportList.error_num}}</p>
    <p class='description'><strong>用例执行情况如下:</strong></p>
    <p id='show_detail_line'>Show
    <el-link type="primary" class="show" @click="showAll()">所有用例</el-link>&nbsp;
    <el-link type="success" class="show" @click="showPass()">只看成功</el-link>&nbsp;
    <el-link type="danger" class="show" @click="showFail()">只看失败</el-link>&nbsp;
    <el-link type="warning" class="show" @click="showError()">只看异常</el-link>
    </p>
</div>
<!-- 饼图图谱 -->
<div class="apps" id="apps"></div>
</div>
<div >
    <table id='result_table'>
        <colgroup>
        <col align='left'/>
        <col align='right'/>
        <col align='right'/>
        <col align='right'/>
        <col align='right'/>
        <col align='right'/>
    </colgroup>
    <tr id='header_row' >
        <td>用例列表</td>
        <td>Count</td>
        <td>Pass</td>
        <td>Fail</td>
        <td>Error</td>
    </tr>
    
    <tr class='passCase' v-for="(item,index) in reportList.content" :key="index" >
        <td v-show="item.result==='pass'">
            <div class='testcase' >{{item.case_name}}</div>

        </td >
        <td v-show="item.result==='pass'" colspan='4' align='center'>pass</td>
    </tr>
    
    <tr class='failCase' v-for="(item,index) in reportList.content" :key="index" >
        <td v-show="item.result==='fail'">
            <div class='testcase'>{{item.case_name}}</div>
        </td>
        <td v-show="item.result==='fail'" colspan='4' align='center' >
            <a class='failCase' @click="showInfo($event)" >fail</a>
            <div class="popup_window" v-for="(step,index) in item.step_list" :key="index">
                <pre class="passCase" v-show="step.result==='pass'">pass  pass<br></pre>
                <pre class="failCase" v-show="step.result==='fail'" >fail  {{step.msg}}<br></pre> 
            </div>
        </td>
    </tr>
    <tr class='errorCase' v-for="(item,index) in reportList.content" :key="index">
        <td v-show="item.result==='error'">
            <div class='testcase'>{{item.case_name}}</div>
        </td>
        <td v-show="item.result==='error'" colspan='4' align='center' >
            <a class='errorCase' @click="showInfo($event)">error</a>
            <div class="popup_window" v-for="(step,index) in item.step_list" :key="index">
                <pre class="passCase" v-if="step.result==='pass'">pass  pass <br></pre>
                <pre class="errorCase" v-if="step.result==='error'">error {{step.msg}}<br></pre>
                    
            </div>
        </td>
    </tr>
    <tr id='total_row'>
        <td>Total</td>
        <td>{{reportList.case_num}}</td>
        <td>{{reportList.pass_num}}</td>
        <td>{{reportList.fail_num}}</td>
        <td>{{reportList.error_num}}</td>
    </tr>
</table>
</div>
</div>
</template>

<script>
import * as echarts from 'echarts'
import {get_report} from '@/api/report'
export default {
  name: 'report',
  data(){
    return {
        plan_id:undefined,
        reportList: [],
        pass_num:null,
        error_num:null,
        fail_num:null
    }
  },
  mounted: function() {
    this.flag=this.$route.query.flag;
    this.id=this.$route.query.id;
    this.showReport();
  },
  methods:{
      showReport(){
          get_report(this.flag,this.id).then((response)=>{
            this.reportList=response.data
            this.pass_num=response.data.pass_num
            this.error_num=response.data.error_num
            this.fail_num=response.data.fail_num
            this.drawCharts()
          })
      },
      back(){
        this.$router.go(-1);//返回上一步
      },
       showInfo(obj) {
        var td_tag = obj.currentTarget.parentNode;
        var details_div = td_tag.lastElementChild;
        var displayState = details_div.style.display;
        if (displayState != 'block') {
            details_div.style.display = 'block';
        }
        else {
            details_div.style.display = 'none'
        }
    },
       showAll() {
        var trs = document.getElementsByTagName("tr");
        for (var i = 1; i < trs.length - 1; i++) {
            trs[i].style.display = 'table-row';
        }
    },
     showPass() {
        var trs = document.getElementsByTagName("tr");
        for (var i = 1; i < trs.length - 1; i++) {
            if (trs[i].className == "passCase") {
                trs[i].style.display = 'table-row';
            }
            else {
                trs[i].style.display = 'none';
            }
        }
    },
     showFail() {
        var trs = document.getElementsByTagName("tr");
        for (var i = 1; i < trs.length - 1; i++) {
            if (trs[i].className == "failCase") {
                trs[i].style.display = 'table-row';
            }
            else {
                trs[i].style.display = 'none';
            }
        }
    },
      showError() {
        var trs = document.getElementsByTagName("tr");
        for (var i = 1; i < trs.length - 1; i++) {
            if (trs[i].className == "errorCase") {
                trs[i].style.display = 'table-row';
            }
            else {
                trs[i].style.display = 'none';
            }
        }
    },
    //饼形图
    drawPieChart(){
        // 绘制图表
        var apps = echarts.init(document.getElementById('apps'))
        var option={
            tooltip: {
            trigger: 'item',
            formatter: "{a}:{b}:({d}%)"
        },
        legend: {

            bottom:10,
            data:['Pass','Fail','Error']
        },
        series: [
            {
                name:'状态',
                type:'pie',
                selectedMode: 'single',
                radius: [0, '70%'],

                label: {
                    normal: {
                        formatter: '{d}%',
                        position: 'inner'
                    }
                },
                data:[
                    {
                        value:this.pass_num,
                        name:'Pass',
                        itemStyle:{
                            normal:{
                                color:'#6c6',
                                shadowBlur:'90',
                                shadowColor:'rgba(0,0,0,0.8)',
                                shadowOffsetY:'30'
                            }
                        }
                    },
                    {
                        value:this.error_num,
                        name:'Error',
                        itemStyle:{
                            normal:{
                                color:'#c60'
                            }
                        }
                    },
                    {
                        value:this.fail_num,
                        name:'Fail',
                        itemStyle:{
                            normal:{
                                color:'#c00'
                            }
                        }
                    }
                ]
            }

        ]
        }
        apps.setOption(option);
    },
    drawCharts(){
        this.drawPieChart()
    }
  }
}
</script>

<style lang="scss" scoped>
        body {
            font-family: verdana, arial, helvetica, sans-serif;
            font-size: 80%;
        }

        table {
            font-size: 90%;
        }

        pre {
        }
        h1 {
            font-size: 16pt;
            color: gray;
        }
        .heading1{
            display: flex;
        }
        .heading {
            margin-top: 3ex;
            margin-left: 3ex;
            margin-bottom: 1ex;
            width: 50%;
        }
        .heading .attribute {
            margin-top: 1ex;
            margin-bottom: 0;
        }
        .heading .description {
            margin-top: 4ex;
            margin-bottom: 6ex;
        }
        a.popup_link {
        }

        a.popup_link:hover {
            color: red;
        }
        .show{
            font-size: 90%;
        }
        .popup_window {
            display: none;
            position: relative;
            left: 0px;
            top: 0px;
            /*border: solid #627173 1px; */
            padding: 10px;
            background-color: #E6E6D6;
            font-family: "Lucida Console", "Courier New", Courier, monospace;
            text-align: left;
            font-size: 8pt;
            width: 700px;
        }


        /* -- report ------------------------------------------------------------------------ */
        #show_detail_line {
            margin-top: 3ex;
        }

        #result_table {
            width: 90%;
            margin-left: 3ex;
            border-collapse: collapse;
            border: 1px solid #777;
        }

        #header_row {
            font-weight: bold;
            color: white;
            background-color: #777;
        }

        #result_table td {
            border: 1px solid #777;
            padding: 2px;
        }

        #total_row {
            font-weight: bold;
        }

        .passClass {
            background-color: #6c6;
        }

        .failClass {
            background-color: #c00; 
        }

        .errorClass {
            background-color: #c60;
        }

        .passCase {
            color: #6c6;
        }

        .failCase {
            color: #c00;
            font-weight: bold;
            word-break: break-all;
           
        }

        .errorCase {
            color: #c60;
            font-weight: bold;
            word-break: break-all;
           
        }

        .hiddenRow {
            display: none;
        }

        .testcase {
            margin-left: 2em;
        }

        #ending {
        }

        .apps{
            height: 270px;
            width: 50%;
            // background-color: pink;
            margin-top: 2ex;
            margin-right: 10px;
            border: 1px solid #fff;
            position: relative;
            top: 0px;
            float: right;
            padding-right: 10px;
            padding-left: 0px;
            margin-bottom: 1ex;
        }
</style>
