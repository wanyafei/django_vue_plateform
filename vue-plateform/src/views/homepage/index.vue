<template>
  <div class="app-container">
  <el-row :gutter="40" class="panel-group">
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('newVisitis')">
        <div class="card-panel-icon-wrapper icon-people">
          <svg-icon icon-class="table" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            <router-link to='/project/project' >
            项目管理
            </router-link>
          </div>
          <div class="card-panel-num" >{{number.project_num}}</div>
        </div>
      </div>
    </el-col> 
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('messages')">
        <div class="card-panel-icon-wrapper icon-message">
          <svg-icon icon-class="tree" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            <router-link to='/environment/environment'>
            环境管理
            </router-link>
          </div>
          <div class="card-panel-num" >{{number.env_num}}</div>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('purchases')">
        <div class="card-panel-icon-wrapper icon-money">
          <svg-icon icon-class="nested" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            <router-link to='/apitest/testcase'>
            测试用例
            </router-link>
          </div>
          <div class="card-panel-num" >{{number.case_num}}</div>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('shoppings')">
        <div class="card-panel-icon-wrapper icon-shopping">
          <svg-icon icon-class="form" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            <router-link to='/testreport/testreport'>
            测试报告
            </router-link>
          </div>
          <div class="card-panel-num" >{{number.report_num}}</div>
        </div>
      </div>
    </el-col>
  </el-row>
  <el-row>
    <el-col><router-link to='/task/task' ><el-link type="primary">查看更多</el-link></router-link></el-col>
  </el-row>
  <el-row class="panel-task">
    <el-col :span="50" class="panel-task-list">
       <el-table
    :data="taskList"
    stripe
    style="width: 100%">
    <el-table-column
      prop="taste_name"
      label="任务名称"
      width="180">
    <template slot-scope="scope"> {{ scope.row.fields.taste_name }} </template>
    </el-table-column>
    <el-table-column
      prop="taste_time"
      label="执行时间"
      width="160">
    <template slot-scope="scope"> {{ scope.row.fields.taste_time }} </template>
    </el-table-column>
    <el-table-column
      prop="status"
      label="状态"
      width="160">
    <template slot-scope="scope"> {{ status_change(scope.row.fields.status) }} </template>
    </el-table-column>
    </el-table>
    <div class="sc-pagination-container" style="margin-left:-9%">
     <ul >
      <el-pagination
        background
        layout="total,prev, pager, next"
        v-show="pagination.total>0"
        :total="pagination.total"
        :page-size="pagination.limit"
        @current-change="handleCurrentChange">
      </el-pagination>
     </ul>
    </div> 
    </el-col>
    <el-col >
      <div id="myChart"></div>
    </el-col>
  </el-row>
  </div>
</template>

<script>
// import CountTo from 'vue-count-to'
import * as echarts from 'echarts'
import {getnumber_prj_env_case_report,get_num_byechart} from '@/api/index'
import {getTask} from '@/api/task'
export default {
  data(){
    return {
      taskList: [],
      report_list:{
        // month:[],
        // pass_num:[],
        // error_num:[],
        // fail_num:[]
      },
      pagination: {
          page: 1,
          limit: 5,
          total: 0
        },
      queryParams: {
          taskname:undefined,
          project:undefined
        },
      number:{
        project_num:null,
        env_num:null,
        case_num:null,
        report_num:null
      }
    }
  },
  mounted: function(){
    this.get_num_byecharts()
    this.getnumber()
    this.showTask()
    
    
  },
  components: {
    // CountTo
  },
  methods: {
    getnumber(){
      getnumber_prj_env_case_report().then((response)=>{
        this.number=response.data
      })
    },
    showTask () {
        this.queryParams.page=this.pagination.page
        this.queryParams.limit=this.pagination.limit
        getTask(this.queryParams).then((response) => {
            this.taskList = response.data.data
            this.pagination.total=response.data.totalCount
        })
        
    },
    get_num_byecharts(){
      get_num_byechart().then((response)=>{
          this.report_list =response.data
          this.drawLine()
      })
    },
    handleSetLineChartData(type) {
      this.$emit('handleSetLineChartData', type)
    },
    handleCurrentChange(val) {
      this.pagination.page = val;
      this.queryParams.page = this.pagination.page;
      this.queryParams.limit = this.pagination.limit;
      getTask(this.queryParams).then((response) => {
            this.taskList = response.data.data
            this.pagination.total=response.data.totalCount
      });
    },
    status_change(val){
        let lab=""
        switch(val){
            case 0:
                lab="STOP"
                break;
            case 1:
                lab="RUNNING"
                break;
            case 2:
                lab="PAUSE"
                break;
            case 3:
                lab="RESUME"
                break;
        }
        return lab
    },
    drawLine(){
      // 选择容器
      let myChart = echarts.init(document.getElementById('myChart'))
      var option= {
        // 组件图例
        legend: {
          data: ['通过','失败','错误'],
          top: 30
        },
        color: ['#6c6','#c00','#c60' ], // 折线图的颜色 有几条设置几个
        //标题
        title: {
          // show: true, // 是否显示组件标题
          text: '测试报告概览', // 标题文本
          top: -6,
          left: 'left',
          textStyle:{
            fontSize: 15,
            color:'#666'
          }
          
        },
        // 提示框组件  鼠标移动到图标上面展示的组件
        tooltip:{
          show: true, // 可以设置是否显示
          trigger: 'axis',//触发类型  参数：axis 主要柱形图 折线图使用 item 散点图 饼图等
          triggerOn: 'mousemove|click', // 提示框触发方式
          // position: [10,10], // 值有两类 Array  和 Function
          axisPointer:{type:'shadow'}, //自动联动展示
          grid: {} }, // 理解了一下就是图标所以区域的节本设置
          // 坐标系中X轴的相关设置
          xAxis: {
            name:'日期',
            data: this.report_list.month
          },
          // 坐标系中y轴的相关设置
          yAxis: {name:'数量'},
          // 图表的主体
          series:[
            {
              name: '通过',
              type: 'bar',
              data: this.report_list.pass_num
                        },
            {
              name: '失败',
              type: 'bar',
              data: this.report_list.error_num
                        },
            {
              name: '错误',
              type: 'bar',
              data: this.report_list.fail_num
                        },
          
          ]
        };
        myChart.setOption(option);  
    }
  }
}
</script>

<style lang="scss" scoped>
#myChart {
        width: 50%;
        min-height: 300px;
        clear: both;
        box-sizing: border-box;
        margin: 1px auto;
        margin-left: 50%;
        margin-top: -30%;
    }
.panel-task{
    background: #fff;
    height: 200px;
    font-size: 0%;
  }
.panel-group {
  margin-top: 18px;
  .card-panel-col {
    margin-bottom: 32px;
  }
  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);
    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }
      .icon-people {
        background: #40c9c6;
      }
      .icon-message {
        background: #36a3f7;
      }
      .icon-money {
        background: #f4516c;
      }
      .icon-shopping {
        background: #34bfa3
      }
    }
    .icon-people {
      color: #40c9c6;
    }
    .icon-message {
      color: #36a3f7;
    }
    .icon-money {
      color: #f4516c;
    }
    .icon-shopping {
      color: #34bfa3
    }
    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }
    .card-panel-icon {
      float: left;
      font-size: 48px;
    }
    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px;
      margin-left: 0px;
      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }
      .card-panel-text:hover{
        background-color: #36a3f7;
      }
      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}



@media (max-width:550px) {
  .card-panel-description {
    display: none;
  }
  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;
    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>
